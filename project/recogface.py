from settings import *
from AcessoVisitante import AcessoVisitante
from mqtt import *

client = mqtt_connect()

# Configurações da janela
Window.clearcolor = (0, 0, 0, 1)
Window.size = (1280, 720)

# Carregamento das imagens para treinamento facial
data_path = 'faces/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

Training_Data, Labels = [], []
for i, file in enumerate(onlyfiles):
    image_path = join(data_path, file)
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


class ReconhecimentoScreen(Screen):
    def __init__(self, capture, fps, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(Label(text="Reconhecimento Facial", size_hint=(0.4, 0.2), font_size=40, pos_hint={'top': 1, 'center_x': 0.5}))
        self.kivy_cv = KivyCV(capture, fps, screen_manager)
        self.add_widget(self.kivy_cv)
        self.add_widget(self.layout)



class KivyCV(Image):
    def __init__(self, capture, fps, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.capture = capture
        self.screen_manager = screen_manager
        self.unrecognized_timer = None  # Timer para controle de delay
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        if self.screen_manager.current == "acessoVisitante":
            self.capture.release()
            Clock.unschedule(self.update)
            return

        ret, frame = self.capture.read()
        if not ret:
            return

        image, face = face_detector(frame)

        try:
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            result = model.predict(face)
            confidence = int(100 * (1 - (result[1]) / 300))
            display_string = f"{confidence}% de similaridade"
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            if confidence >= 85:
                cv2.putText(image, "IDENTIFICADO", (220, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                client.publish(MQTT_TOPIC_LIBERAR_MORADOR, "true")
                mqtt_out(client, MQTT_TOPIC_LIBERAR_MORADOR)
                print("Liberando morador")

                if self.unrecognized_timer:
                    Clock.unschedule(self.unrecognized_timer)  # Cancela o redirecionamento
                    self.unrecognized_timer = None

            else:
                self.schedule_unrecognized_redirect()

        except Exception:
            self.schedule_unrecognized_redirect()

        buf = cv2.flip(frame, 0).tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def schedule_unrecognized_redirect(self):
        if not self.unrecognized_timer:
            self.unrecognized_timer = Clock.schedule_once(self.redirect_to_acesso_visitante, 5)  # Delay de 3 segundos

    def redirect_to_acesso_visitante(self, *args):
        print("Redirecionando para acesso visitante após falha de reconhecimento")
        client.publish(MQTT_TOPIC_SOLICITACAO_ENTRADA, "false")
        mqtt_out(client, MQTT_TOPIC_SOLICITACAO_ENTRADA)
        self.screen_manager.current = "acessoVisitante"


class SISTEMA(App):
    def build(self):
        sm = ScreenManager()
        capture = cv2.VideoCapture(0)
        sm.add_widget(ReconhecimentoScreen(capture, 30, sm, name='reconhecimento'))
        sm.add_widget(AcessoVisitante(name='acessoVisitante'))
        return sm


if __name__ == "__main__":
    SISTEMA().run()