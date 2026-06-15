from pydantic import BaseModel
from typing import Dict, List, Union, Optional

# -----Creamos el esqueleto del manifiesto-------

# METADATA
class Metadata(BaseModel):
    title: str
    description: str
    version: str = "1.0"

# INPUTS
class InputParameter(BaseModel):
    type: str = "FLOAT32"
    unit: str
    minimum: float
    maximum: float
    default: float
    currentValue: float
    description: str

class SensorInputs(BaseModel):
    alert: InputParameter
    min_range: InputParameter 
    max_range: InputParameter 

# OUTPUT
class OutputParameter(BaseModel):
    type: str = "FLOAT32"
    unit: str
    description: Optional[str] = None
    dimensions: Optional[int] = None
    resolution: Optional[float] = None
    resolution_bits: Optional[int] = None


class SensorOutputs(BaseModel):
    time_vector: OutputParameter = OutputParameter(type="UNIT32",unit="ms",description="Base temporal asociada a las muestras adquiridas.")
    output_01: OutputParameter 
    output_02: OutputParameter 
    output_03: OutputParameter 

# ACTIONS
class ActionArgument(BaseModel):
    type: str = "UINT16"
    unit: Optional[str] = "Hz"
    type_control: str = "select"
    options: List[Union[int, str]] = [100, 400, 800, 1600]
    default: Union[int, float, str] = 100

class Action(BaseModel):
    description: str
    arguments: Dict[str, ActionArgument] = {} 

class SensorActions(BaseModel):
    init: Action = Action(description="Inicializa el hardware del sensor.",arguments={})
    capture_single: Action = Action(description="Inicia la captura continua devolviendo exclusivamente el primer flujo de datos (output_01).",arguments={"frequency": ActionArgument(options=[100, 400, 800, 1600], default=100)})
    capture_doble: Action = Action(description="Inicia la captura sincronizada devolviendo de forma fija los dos primeros flujos de datos.",arguments={"frequency": ActionArgument(options=[100, 400, 800], default=400)})
    capture_triple: Action = Action(description="Inicia la captura sincronizada completa devolviendo de forma fija los tres flujos de datos.",arguments={"frequency": ActionArgument(options=[100, 400, 800], default=400)})
    stop: Action = Action(description="Detiene cualquier modo de captura activo.",arguments={})
    status: Action = Action(description="Solicita un informe de estado.",arguments={})

# EVENTS
class Event(BaseModel):
    description: str

class SensorEvents(BaseModel):
    hardware_fault: Event = Event(description="Fallo crítico detectado en el hardware.")
    value_alert: Event = Event(description="Valor superior al umbral configurado.")

# TELEMETRY
class Telemetry(BaseModel):
    topic:str = "sensors/sensorId/data"
    format: str = "json"

# MANIFEST
class SensorManifest(BaseModel):
    sensorId: str
    metadata: Metadata
    inputs: SensorInputs
    outputs: SensorOutputs
    actions: SensorActions
    events: SensorEvents
    telemetry: Telemetry


# -----------Creamos el modelo del sensor--------
class SensorCaptureCommand(BaseModel):
    sensorId: str
    minimo: float
    maximo: float
    alerta: float
    modo: str
    frecuencia: int
    tipo: str
    unidad: str