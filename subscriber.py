import paho.mqtt.client as mqtt
import ssl

# Parámetros de conexión al broker MQTT
BROKER = "f3f3e3d73aed48d981bb05a512e52232.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "usuarioSensor"
PASSWORD = "Sensor1234!"
# Carpeta de suscripción del cliente
TOPIC = "sensores/#"

# Función de conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con código:", rc)
    client.subscribe(TOPIC)

# Función cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

# Creación y configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

# Bucle infinito que mantiene la escucha activa del mensaje
client.loop_forever()