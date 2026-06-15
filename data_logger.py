import paho.mqtt.client as mqtt
import ssl
import json
from datetime import datetime, timezone
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Parámetros de conexión al broker MQTT
BROKER = "f3f3e3d73aed48d981bb05a512e52232.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "usuarioSensor"
PASSWORD = "Sensor1234!"
# Carpeta de suscripción del cliente
TOPIC = "sensores/data"

# Configuración InfluxDB
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "_nR3rOihgogRd_LyjTkNPvQmYucnL5x7WDnsU_nnWK914eCuUSsAQVDmLGMX_mMMCHCKa_pqBK1Ywf0VloC_Jw=="
INFLUX_ORG = "tfg"
INFLUX_BUCKET = "sensores"
influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

# Cliente InfluxDB
write_api = influx_client.write_api()

# Función encargada de procesar el mensaje (dato recopilado)
def procesar_mensaje(topic, payload):
    try:
        # Conseguimos el JSON
        data = json.loads(payload)

        # Comprobamos que existen los valores del JSON
        if "sensor_id" not in data or "valor_x" not in data:
            print("Mensaje inválido:", data)
            return None

        # Procesamos el mensaje como queremos 
        registro = {
            "sensor_id": data["sensor_id"],
            "tipo": data.get("tipo", "desconocido"),
            "valor_x": data["valor_x"],
            "valor_y": data.get("valor_y", 0.0),
            "valor_z": data.get("valor_z", 0.0),
            "unidad": data.get("unidad", 0.0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topic": topic
        }

        return registro

    except json.JSONDecodeError:
        print("Error al decodificar JSON:", payload)
        return None

# Función encargada de almacenar el mensaje
def guardar_dato(registro):
    try:

        # Creamos la estructura para guardarlo en la base de datos
        punto = (
            Point(registro["tipo"])
            .tag("sensor_id", registro["sensor_id"])
            .field("valor_x", float(registro["valor_x"]))
            .field("valor_y", float(registro["valor_y"]))
            .field("valor_z", float(registro["valor_z"]))
            .time(registro["timestamp"])
        )

        # Escribimos en base de datos
        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=punto
        )

        print("Guardado en InfluxDB:", registro)

    except Exception as e:
        print("Error al guardar en InfluxDB:", e)


# Función de conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Data Logger conectado al broker")
        client.subscribe(TOPIC)
    else:
        print("Error de conexión:", rc)

# Función cuando se recibe un mensaje
def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    print(f"\nMensaje recibido en {msg.topic}: {payload}")

    # Procesar mensaje
    registro = procesar_mensaje(msg.topic, payload)

    # Guardar si es válido
    if registro:
        guardar_dato(registro)


# Creación y configuración del cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
print("Iniciando Data Logger...")
client.loop_forever()