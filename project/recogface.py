import kivy

kivy.require('1.9.1')

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import paho.mqtt.client as mqtt

# Configurações do MQTT
MQTT_BROKER = "broker.hivemq.com"  # Broker público HiveMQ
MQTT_PORT = 1883  # Porta do broker MQTT
MQTT_TOPIC_LIBERAR_MORADOR = "portaria/morador/entrada"
MQTT_TOPIC_LIBERAR_VISITANTE = "portaria/visitante/entrada"
MQTT_TOPIC_SOLICITACAO_ENTRADA = "portaria/liberar/acesso"
MQTT_TOPIC_SOLICITACAO_NEGADA = "portaria/negar/acesso"

# Função chamada quando a conexão com o broker é estabelecida
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
    else:
        print(f"Falha na conexão. Código de erro: {rc}")

# Função chamada quando uma mensagem é recebida (não será usada neste caso, mas é boa prática)
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Conectar ao broker MQTT
client.loop_start()

# COR DA JANELA E TAMANHO
Window.clearcolor = (0, 0, 0, 1)
Window.size = (1280, 720)

# DIRETORIO DAS IMAGENS
data_path = 'faces/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# TREINAMENTO FACES
Training_Data, Labels = [], []
for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("TREINAMENTO EFETUADO")

face_classifier = cv2.CascadeClassifier('lib/haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return img, []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi

# CAMERA NO KIVY CONFIGURAÇÃO
class KivyCV(Image):
    def __init__(self, capture, fps, **kwargs):
        Image.__init__(self, **kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    # CONFIGURAÇÃO PARA DETECTAR FACE
    def update(self, dt):
        ret, frame = self.capture.read()
        image, face = face_detector(frame)
        try:
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            result = model.predict(face)
            if result[1] < 500:
                confidence = int(100 * (1 - (result[1]) / 300))
                display_string = str(confidence) + '% de similaridade'
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            if confidence >= 85:
                cv2.putText(image, "IDENTIFICADO", (220, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                client.publish(MQTT_TOPIC_LIBERAR_MORADOR, "Reconhecimento bem-sucedido!")
                print(f"Liberando...")
                pass 

        except Exception as e:
                cv2.putText(image, "BLOQUEADO", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                client.publish(MQTT_TOPIC_SOLICITACAO_ENTRADA, "Solicitando entrada")
                pass

        buf = cv2.flip(frame, 0).tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

# Função para finalizar a conexão do MQTT ao final
def on_stop():
    client.loop_stop()

client.on_stop = on_stop

# FUNÇÃO DO SCREAN PARA MUDAR DE TELA
class SISTEMA(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FunctionScreen(name='functionScreen'))
        return sm

# PRIMEIRA TELA DO SUB-SCREEN
class FunctionScreen(Screen):
    def __init__(self, **kwargs):
        super(FunctionScreen, self).__init__(**kwargs)
        layout2 = FloatLayout()
        tituloscreen2 = Label(text='RECONHECIMENTO\nPOSICIONE SEU ROSTO NO SENSOR',
                              halign='center', valign='center', size_hint=(0.4, 0.2),
                              font_size=40, font_name='Roboto-Bold', color=[1, 1, 1, 1], pos_hint={'top': 1, 'center_x': 0.5})

        # CONFIGURAÇÃO DO FLOATLAYOUT
        self.add_widget(layout2)

        # CONFIGURAÇÃO DA CAMERA
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCV(capture=self.capture, fps=60)
        self.my_camera.size_hint = (1, 1)
        self.my_camera.pos_hint = {'x': 0, 'y': .0}

        # LAYOUT PARA MOSTRAR OS WIDGET NA TELA
        layout2.add_widget(tituloscreen2)
        layout2.add_widget(self.my_camera) 

# FIM DO SISTEMA
if __name__ == '__main__':
    SISTEMA().run()
