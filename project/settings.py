import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
