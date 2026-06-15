import ssl
import json
import time
import paho.mqtt.client as mqtt
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.sensor_schema import SensorManifest, SensorCaptureCommand
from app.models.sensor import Sensor
from app.db.fake_db import sensors_db
from app.services.manifest_service import generar_manifest

router = APIRouter()

# Parámetros de conexión al broker MQTT
MQTT_BROKER = "f3f3e3d73aed48d981bb05a512e52232.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USERNAME = "usuarioSensor"
MQTT_PASSWORD = "Sensor1234!"

# Funcion que inicia la captura de datos
def enviar_inicio_hivemq(sensor: SensorCaptureCommand):
    try:
        # Crea la conexion
        client = mqtt.Client(client_id=sensor.sensorId)
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        client.connect(MQTT_BROKER, MQTT_PORT)

        # Configura el mensaje
        info_sensor = {
            "accion": "START",
            "sensorId" : sensor.sensorId,
            "minimo": sensor.minimo,
            "maximo": sensor.maximo,
            "alerta": sensor.alerta,
            "modo": sensor.modo,
            "frecuencia": sensor.frecuencia,
            "tipo": sensor.tipo,
            "unidad": sensor.unidad
        }
        topic = f"sensores/{sensor.sensorId}/cmd"

        # Manda el mensaje
        client.publish(topic, json.dumps(info_sensor), qos=1).wait_for_publish()
        print(f"[FastAPI -> HiveMQ] Comando publicado en {topic}: {info_sensor}")

        client.disconnect()
        time.sleep(0.2)

    except Exception as e:
        print(f"Error enviado por MQTT a HiveMQ: {e}")


# Funcion que termina la captura de datos
def enviar_fin_hivemq(sensorID: str):
    try:
        # Crea la conexion
        client = mqtt.Client(client_id=sensorID)
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        client.connect(MQTT_BROKER, MQTT_PORT)

        # Configura el mensaje
        info_sensor = {
            "accion":"STOP"
        }
        topic = f"sensores/{sensorID}/cmd"

        # Manda el mensaje
        client.publish(topic, json.dumps(info_sensor), qos=1).wait_for_publish()
        print(f"[FastAPI -> HiveMQ] Comando publicado en {topic}: {info_sensor}")

        client.disconnect()
        time.sleep(0.2)

    except Exception as e:
        print(f"Error enviado por MQTT a HiveMQ: {e}")


# Crear el sensor
@router.post("/sensors")
def create_sensor(manifest: SensorManifest):
    if manifest.sensorId in sensors_db:
        raise HTTPException(status_code=400, detail="Sensor ya existe")

    nuevo_sensor = Sensor(
        manifest=manifest
    )

    sensors_db[manifest.sensorId] = nuevo_sensor
    return {"message": "Sensor creado"}

# Obtiene lista de identifiadores de sensores
@router.get("/sensors")
def get_sensors():
    return list(sensors_db.keys())

# Obtener el manifiesto seegun el identificador del sensor
@router.get("/sensors/{sensor_id}/manifest")
def get_manifest(sensor_id: str):
    if sensor_id not in sensors_db:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")

    return sensors_db[sensor_id].manifest

# Comenzar la captura de los datos
@router.post("/sensors/start-capture")
def start_capture(listaSensoresActivos: list[SensorCaptureCommand], background_tasks:BackgroundTasks):
    for sensor in listaSensoresActivos:
        print(f"Iniciando hardware de: {sensor.sensorId}")
        background_tasks.add_task(enviar_inicio_hivemq, sensor)

    return {"status": "success", "message": "Captura del sistema iniciada de forma centralizada"}

# Detener la captura de los datos
@router.post("/sensors/stop-capture")
def end_capture(listaSensoresActivos: list[SensorCaptureCommand], background_tasks:BackgroundTasks):
    for sensor in listaSensoresActivos:
        background_tasks.add_task(enviar_fin_hivemq, sensor.sensorId)

    return {"status": "success", "message": "Fin de la captura de datos"}

    