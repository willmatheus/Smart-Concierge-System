from settings import *

def mqtt_connect():
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
    return client

def mqtt_out(client, topic):
    client.publish(topic)
    return
