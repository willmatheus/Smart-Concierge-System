import cv2
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput

kivy.require('1.9.1')

# Configurações da janela
Window.clearcolor = (0.2, 0.2, 0.3, 1)  # Fundo com tema moderno
Window.size = (980, 720)

# Classe para capturar a câmera
class KivyCV(Image):
    def __init__(self, capture, fps, **kwargs):
        super().__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            buf = cv2.flip(frame, 0).tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

# Tela inicial
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Título
        title = Label(
            text="SISTEMA DE CADASTRO",
            font_size="40sp",
            bold=True,
            color=[1, 1, 1, 1],
            size_hint=(1, 0.2),
            pos_hint={"top": 1},
        )

        # Subtítulo
        subtitle = Label(
            text="Cadastre e registre faces para reconhecimento",
            font_size="20sp",
            color=[1, 1, 1, 0.8],
            size_hint=(1, 0.1),
            pos_hint={"top": 0.85},
        )

        # Campos de entrada
        name_label = Label(text="Nome:", font_size="18sp", color=[1, 1, 1, 1], size_hint=(0.2, 0.1), pos_hint={"x": 0.1, "y": 0.6})
        self.name_input = TextInput(multiline=False, size_hint=(0.6, 0.1), pos_hint={"x": 0.3, "y": 0.6})

        cpf_label = Label(text="CPF:", font_size="18sp", color=[1, 1, 1, 1], size_hint=(0.2, 0.1), pos_hint={"x": 0.1, "y": 0.5})
        self.cpf_input = TextInput(multiline=False, size_hint=(0.6, 0.1), pos_hint={"x": 0.3, "y": 0.5})

        ap_label = Label(text="Apartamento:", font_size="18sp", color=[1, 1, 1, 1], size_hint=(0.2, 0.1), pos_hint={"x": 0.1, "y": 0.4})
        self.ap_input = TextInput(multiline=False, size_hint=(0.6, 0.1), pos_hint={"x": 0.3, "y": 0.4})

        # Botões
        button_layout = BoxLayout(orientation="horizontal", size_hint=(0.8, 0.9), pos_hint={"center_x": 0.5, "y": 0.2}, spacing=20)
        photo_button = Button(text="Tirar Fotos", size_hint=(0.3, 0.1), background_color=[0.1, 0.6, 0.6, 1], on_press=self.take_photo)
        register_button = Button(text="Cadastrar", size_hint=(0.3, 0.1), background_color=[0.0, 0.6, 0.0, 1], on_press=self.register)

        button_layout.add_widget(photo_button)
        button_layout.add_widget(register_button)

        # Adiciona widgets ao layout
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(cpf_label)
        layout.add_widget(self.cpf_input)
        layout.add_widget(ap_label)
        layout.add_widget(self.ap_input)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def take_photo(self, instance):
        self.manager.current = "functionScreen"

    def register(self, instance):
        name = self.name_input.text
        cpf = self.cpf_input.text
        ap = self.ap_input.text
        print(f"Nome: {name}, CPF: {cpf}, Apartamento: {ap}")

# Tela de funcionalidade
class FunctionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Texto explicativo
        instruction = Label(
            text="Registre as faces capturando fotos.\nPressione 'Voltar' após capturar as imagens.",
            font_size="18sp",
            halign="center",
            valign="middle",
            color=[1, 1, 1, 1],
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "top": 0.9},
        )

        # Botões
        photo_button = Button(text="Tirar Fotos", size_hint=(0.3, 0.1), pos_hint={"x": 0.1, "y": 0.1}, background_color=[0.1, 0.6, 0.6, 1])
        back_button = Button(text="Voltar", size_hint=(0.3, 0.1), pos_hint={"x": 0.6, "y": 0.1}, background_color=[0.8, 0.2, 0.2, 1])

        photo_button.bind(on_press=self.capture_photos)
        back_button.bind(on_press=self.go_back)

        # Adiciona widgets ao layout
        layout.add_widget(instruction)
        layout.add_widget(photo_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def capture_photos(self, instance):
        print("Capturando fotos...")

    def go_back(self, instance):
        self.manager.current = "welcomeScreen"

# Gerenciador de telas
class SISTEMA(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcomeScreen"))
        sm.add_widget(FunctionScreen(name="functionScreen"))
        return sm

# Executa o aplicativo
if __name__ == "__main__":
    SISTEMA().run()
