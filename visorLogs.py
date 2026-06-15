import paho.mqtt.client as mqtt
import time
import random
import ssl
import json
import requests

# Parámetros de conexión al broker MQTT
BROKER = "f3f3e3d73aed48d981bb05a512e52232.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "usuarioSensor"
PASSWORD = "Sensor1234!"
# Identificador del sensor
SENSOR_ID = "sensor01"
# Configuración del backend
API_URL = "http://127.0.0.1:8000"

# Topics usados
TOPIC_LOG = f"sensores/logs"

# Función de conexión con el broker MQTT (cliente, usuario, información sobre conexión, código resultado)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC_LOG)
        print(f"Suscrito a {TOPIC_LOG}")
    else:
        print("Error de conexión:", rc)

# Función de mensaje con el broker MQTT
def on_message(client, userdata, msg):
    try:
        # Obtenemos el log e imprimir        
        log = msg.payload.decode()
        print(log)

    except Exception as e:
        print("Error de mensaje: ", e)


# Creación y configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_start()
print(f"Esperando logs...")

try:
    while True:
        # Un bucle vacío sutil que mantiene el proceso abierto consumiendo mínimo recurso
        pass
except KeyboardInterrupt:
    print("\n[*] Visor de logs detenido por el usuario. Cerrando conexiones...")
    client.loop_stop()
    client.disconnect()