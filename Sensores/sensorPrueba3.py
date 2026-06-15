import paho.mqtt.client as mqtt
import datetime
import time
import random
import ssl
import json
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env automáticamente
load_dotenv()

# Parámetros de conexión recuperados del entorno global
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT", 8883))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

# Identificador del sensor
SENSOR_ID = "sensor03"

# Configuración del backend
API_URL = os.getenv("API_URL")

# Variables de estado dinámicas (parámetros usuario)
ACTIVADO = False
FRECUENCIA = 1.0
MODO = "capture_single"
VAL_MIN = 0.0
VAL_MAX = 30.0
VAL_ALERT = 25.0
TIPO = ""
UNIDAD = ""

# Topics usados
TOPIC_TELEMETRIA = os.getenv("TOPIC_TELEMETRIA", "sensores/data")
TOPIC_COMANDOS = f"sensores/{SENSOR_ID}/cmd"
TOPIC_LOG = os.getenv("TOPIC_LOG", "sensores/logs")


# Función de conexión con el broker MQTT (cliente, usuario, información sobre conexión, código resultado)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Sensor {SENSOR_ID} conectado al broker MQTT")
        client.subscribe(TOPIC_COMANDOS)
        print(f"Suscrito a {TOPIC_COMANDOS}")
    else:
        print("Error de conexión:", rc)

# Función de mensaje con el broker MQTT
def on_message(client, userdata, msg):
    # Se declaran variable globales para modificarlas desde aqui
    global ACTIVADO, FRECUENCIA, MODO, VAL_MIN, VAL_MAX, VAL_ALERT, TIPO, UNIDAD
    try:
        
        # Obtenemos el mensaje y los parámetros        
        info_sensor = json.loads(msg.payload.decode())
        print(f"Mensaje recibido {info_sensor}")
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Detenemos el sensor
        if(info_sensor["accion"] == "STOP"):

            # Log detener
            log = f"[{ts}] [SUCCESS] [{SENSOR_ID}] Adquisición DETENIDA. Hardware en modo espera."
            print(log)
            client.publish(TOPIC_LOG, log)
            ACTIVADO = False

        # Iniciamos el sensor
        elif (info_sensor["accion"] == "START"):

            # Capturamos parámetros de configuración
            hz = info_sensor["frecuencia"]
            FRECUENCIA = hz / 100
            MODO = info_sensor["modo"]
            VAL_MIN = info_sensor["minimo"]
            VAL_MAX = info_sensor["maximo"]
            VAL_ALERT = info_sensor["alerta"]
            TIPO = info_sensor["tipo"]
            UNIDAD = info_sensor["unidad"]
            ACTIVADO = True

            # Log iniciar
            log = f"[{ts}] [SUCCESS] [{SENSOR_ID}] Captura INICIADA con éxito. Hardware en modo captura."
            print(log)
            client.publish(TOPIC_LOG, log)

    except Exception as e:
            # Log error
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log = f"[{ts}] [ERROR] [{SENSOR_ID}] Error procesando comando MQTT: {e}"
            print(log)
            client.publish(TOPIC_LOG, log)


# Creación y configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_start()
print(f"Esperando ordenes desde el control {SENSOR_ID}...")

# Simulador de envío periódico de datos
try:
    while True:
        if ACTIVADO:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            if MODO == "capture_doble":
                # Generamos el valor random
                valor_x = round(random.uniform(VAL_MIN, VAL_MAX), 2)
                valor_y = round(random.uniform(VAL_MIN, VAL_MAX), 2)
                
                # Mensaje
                mensaje = {
                    "sensor_id": SENSOR_ID,
                    "tipo": TIPO,
                    "unidad": UNIDAD,
                    "valor_x": valor_x,
                    "valor_y": valor_y
                }
                
                # Publicación del mensaje en la carpeta definida
                client.publish(TOPIC_TELEMETRIA, json.dumps(mensaje))
                print("Enviado:", mensaje)

                time.sleep(FRECUENCIA)

            else:
                log = f"[{ts}] [ERROR] [{SENSOR_ID}] Modo {MODO} no soportado por el sensor."
                print(log)
                client.publish(TOPIC_LOG, log)
                ACTIVADO = False

        else:
            # Si no esta activado, dormimos el proceso para no saturar CPU
            time.sleep(1)
            
except KeyboardInterrupt:
    print("Deteniendo captura...")
    client.loop_stop()
    client.disconnect()