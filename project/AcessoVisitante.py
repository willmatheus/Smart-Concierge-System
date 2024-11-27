from settings import *
# from recogface import client
# from mqtt import *

class AcessoVisitante(Screen):
    def __init__(self, **kwargs):
        super(AcessoVisitante, self).__init__(**kwargs)
        layout1 = FloatLayout()

        self.title1 = Label(text='Visita', font_size='50sp', color=[1, 1, 1, 1],
                            font_name='Roboto-Bold', size_hint=(None, None), size=(700, 100), pos_hint={'x': 0.15, 'top': 0.85})

        self.username = TextInput(hint_text="Nome", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                                  background_normal='', background_active='',
                                  foreground_color=[0.1, 0.1, 0.1, 1], padding=10, pos_hint={'x': 0.15, 'y': 0.6})
        self.username.border = [0, 0, 0, 0]

        self.cpf = TextInput(hint_text="CPF", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                             background_normal='', background_active='', foreground_color=[0.1, 0.1, 0.1, 1], padding=10,
                             pos_hint={'x': 0.15, 'y': 0.5})
        self.cpf.border = [0, 0, 0, 0]

        self.apartamento = TextInput(hint_text="Apartamento Visita", multiline=False, size_hint=(0.7, None), height=45, font_size=18,
                                      background_normal='', background_active='', foreground_color=[0.1, 0.1, 0.1, 1], padding=10,
                                      pos_hint={'x': 0.15, 'y': 0.4})
        self.apartamento.border = [0, 0, 0, 0]

        CANCELAR = Button(text='CANCELAR', on_press=self.cancelar, size_hint=(0.4, None), height=50, font_size=18,
                      background_color=[1, 0, 0, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.05, 'y': 0.2})

        SOLICITAR = Button(text='SOLICITAR', on_press=self.solicitar, size_hint=(0.4, None), height=50, font_size=18,
                           background_color=[0.4, 0.4, 0.8, 1], color=[1, 1, 1, 1], pos_hint={'x': 0.55, 'y': 0.2})

        layout1.add_widget(self.title1)
        layout1.add_widget(self.username)
        layout1.add_widget(self.cpf)
        layout1.add_widget(self.apartamento)
        layout1.add_widget(CANCELAR)
        layout1.add_widget(SOLICITAR)

        self.add_widget(layout1)

    def cancelar(self, instance):
        print('Você foi para a tela principal')
        self.manager.current = 'welcomeScreen'

    def solicitar(self, instance):
        name = self.username.text
        cpf = self.cpf.text
        apartamento = self.apartamento.text
        # mqtt_out(MQTT_TOPIC_LIBERAR_VISITANTE, client)
        print("Nome:", name, "\nCPF:", cpf, "\nApartamento:", apartamento)
        print('Solicitação efetuada com sucesso')

class INTERFACE(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AcessoVisitante(name='acessoVisitante'))
        return sm
    
if __name__ == '__main__':
    INTERFACE().run()