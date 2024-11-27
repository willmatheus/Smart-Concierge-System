from settings import *

# COR DA JANELA E TAMANHO
Window.clearcolor = (0.9, 0.9, 0.9, 1)  # Cor mais suave para o fundo
Window.size = (980, 720)

# CAMERA NO KIVY CONFIGURAÇÃO
class KivyCV(Image):
    def __init__(self, capture, fps, **kwargs):
        Image.__init__(self, **kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceCascade = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

# FUNÇÃO DO SCREAN PARA MUDAR DE TELA
class SISTEMA(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcomeScreen'))
        sm.add_widget(FunctionScreen(name='functionScreen'))
        return sm

# PRIMEIRA TELA DO SUB-SCREEN
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout1 = FloatLayout()

        # Título melhorado com uma cor mais neutra
        self.title1 = Label(text='SISTEMA DE CADASTRO', font_size='50sp', color=[0.2, 0.2, 0.8, 1],
                            font_name='Roboto-Bold', size_hint=(None, None), size=(700, 100), pos_hint={'x': 0.15, 'top': 0.85})

        # Descrição mais suave e moderna
        tituloscreen1 = Label(text='CLIQUE EM FOTOS PARA CADASTRAR AS FACES PARA O RECONHECIMENTO', color=[0.3, 0.3, 0.3, 1],
                              halign='center', font_name='Roboto-Regular', valign='center', size_hint=(0.9, 0.15),
                              pos_hint={'x': 0.05, 'top': 0.77})

        # Campos de entrada compactos
        self.username = TextInput(hint_text="Nome", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                                  background_normal='', background_active='',
                                  foreground_color=[0.1, 0.1, 0.1, 1], padding=10, pos_hint={'x': 0.15, 'y': 0.6})
        self.username.border = [0, 0, 0, 0]

        self.cpf = TextInput(hint_text="CPF", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                             background_normal='', background_active='', foreground_color=[0.1, 0.1, 0.1, 1], padding=10,
                             pos_hint={'x': 0.15, 'y': 0.5})
        self.cpf.border = [0, 0, 0, 0]

        self.apartamento = TextInput(hint_text="Apartamento", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                                      background_normal='', background_active='', foreground_color=[0.1, 0.1, 0.1, 1], padding=10,
                                      pos_hint={'x': 0.15, 'y': 0.4})
        self.apartamento.border = [0, 0, 0, 0]

        # Botões modernos
        FOTO = Button(text='TIRAR FOTOS', on_press=self.tirarfoto, size_hint=(0.4, None), height=50, font_size=18,
                      background_color=[0.3, 0.6, 0.3, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.05, 'y': 0.2})

        CADASTRAR = Button(text='CADASTRAR', on_press=self.cadastrar, size_hint=(0.4, None), height=50, font_size=18,
                           background_color=[0.4, 0.4, 0.8, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.55, 'y': 0.2})

        # Layout do welcome screen
        layout1.add_widget(self.title1)
        layout1.add_widget(tituloscreen1)
        layout1.add_widget(self.username)
        layout1.add_widget(self.cpf)
        layout1.add_widget(self.apartamento)
        layout1.add_widget(FOTO)
        layout1.add_widget(CADASTRAR)

        self.add_widget(layout1)

    def tirarfoto(self, instance):
        print('Você foi para a tela 2')
        self.manager.current = 'functionScreen'

    def cadastrar(self, instance):
        name = self.username.text
        cpf = self.cpf.text
        apartamento = self.apartamento.text
        print("Nome:", name, "\nCPF:", cpf, "\nApartamento:", apartamento)
        print('Cadastro efetuado com sucesso')

# SEGUNDA TELA DO SCREEN
class FunctionScreen(Screen):
    def __init__(self, **kwargs):
        super(FunctionScreen, self).__init__(**kwargs)
        layout2 = FloatLayout()

        # Título
        tituloscreen2 = Label(text='CLIQUE NO BOTÃO FOTOS PARA REGISTRAR AS FACES\nATENÇÃO APÓS TIRAR AS 30 FOTOS CLIQUE EM VOLTAR',
                              halign='center', font_name='Roboto-Regular', size_hint=(0.9, 0.15), color=[0.3, 0.3, 0.3, 1],
                              pos_hint={'x': 0.05, 'top': 0.9})

        # Botões de ação
        self.botaoClick1 = Button(text='VOLTAR', on_press=self.voltar, size_hint=(0.3, None), height=50, font_size=18,
                                  background_color=[0.8, 0.4, 0.4, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.35, 'y': 0.2})

        self.botaoClick2 = Button(text='TIRAR FOTOS', on_press=self.fotofaces, size_hint=(0.3, None), height=50, font_size=18,
                                  background_color=[0.4, 0.7, 0.4, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.35, 'y': 0.35})

        layout2.add_widget(tituloscreen2)
        layout2.add_widget(self.botaoClick1)
        layout2.add_widget(self.botaoClick2)

        self.add_widget(layout2)

    def voltar(self, *args):
        self.manager.current = 'welcomeScreen'

    def fotofaces(self, *args):

        def face_extractor(img):
            face_classifier = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray,1.3,5)

            if faces is():
                return None

            for(x,y,w,h) in faces:
                cropped_face = img[y:y+h, x:x+w]

            return cropped_face


        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count+=1
                face = cv2.resize(face_extractor(frame),(200,200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_name_path = 'faces/user'+str(count)+'.jpg'
                cv2.imwrite(file_name_path,face)

                cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.imshow('Face Cropper',face)
            else:
                print("Face not Found")
                pass

            if cv2.waitKey(1)==13 or count==100:
                break

        cap.release()
        cv2.destroyAllWindows()
        print('Colleting Samples Complete!!!')
        
# FIM DO SISTEMA
if __name__ == '__main__':
    SISTEMA().run()
