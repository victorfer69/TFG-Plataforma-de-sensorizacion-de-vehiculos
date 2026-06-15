from app.schemas.sensor_schema import SensorManifest

# Define como es un sensor dentro del sistema
class Sensor:
    def __init__(self, manifest:SensorManifest):
        self.manifest = manifest