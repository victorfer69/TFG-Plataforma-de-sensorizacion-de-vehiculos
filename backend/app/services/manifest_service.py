from app.schemas.sensor_schema import SensorManifest

# Genera la estructura del manifiesto del sensor
def generar_manifest(sensor: SensorManifest):

    return SensorManifest(
        sensorId=sensor.sensorId,

        metadata={
            "title": sensor.metadata.title,
            "description": sensor.metadata.description,
            "version": sensor.metadata.version
        },

        inputs={

            "alert": {
                "type": sensor.inputs.alert.type,
                "unit": sensor.inputs.alert.unit,
                "minimum": sensor.inputs.alert.minimum,
                "maximum": sensor.inputs.alert.maximum,
                "default": sensor.inputs.alert.default,
                "currentValue": sensor.inputs.alert.currentValue,
                "description": sensor.inputs.alert.description
            },
            "min_range": {
                "type": sensor.inputs.min_range.type,
                "unit": sensor.inputs.min_range.unit,
                "minimum": sensor.inputs.min_range.minimum,
                "maximum": sensor.inputs.min_range.maximum,
                "default": sensor.inputs.min_range.default,
                "currentValue": sensor.inputs.min_range.currentValue,
                "description": sensor.inputs.min_range.description
            },
            "max_range": {
                "type": sensor.inputs.max_range.type,
                "unit": sensor.inputs.max_range.unit,
                "minimum": sensor.inputs.max_range.maximum,
                "maximum": sensor.inputs.max_range.minimum,
                "default": sensor.inputs.max_range.default,
                "currentValue": sensor.inputs.max_range.currentValue,
                "description": sensor.inputs.max_range.description
            }

        },

        outputs={

            "time_vector": {
                "type": sensor.outputs.time_vector.type,
                "unit": sensor.outputs.time_vector.unit,
                "description": sensor.outputs.time_vector.description
            },
            "output_01": {
                "type": sensor.outputs.output_01.type,
                "unit": sensor.outputs.output_01.unit, 
                "dimensions": sensor.outputs.output_01.dimensions,
                "resolution": sensor.outputs.output_01.resolution,
                "resolution_bits": sensor.outputs.output_01.resolution_bits,
                "description": sensor.outputs.output_01.description
            },
            "output_02": {
                "type": sensor.outputs.output_02.type,
                "unit": sensor.outputs.output_02.unit, 
                "dimensions": sensor.outputs.output_02.dimensions,
                "resolution": sensor.outputs.output_02.resolution,
                "resolution_bits": sensor.outputs.output_02.resolution_bits,
                "description": sensor.outputs.output_02.description
            },
            "output_03": {
                "type": sensor.outputs.output_03.type,
                "unit": sensor.outputs.output_03.unit, 
                "dimensions": sensor.outputs.output_03.dimensions,
                "resolution": sensor.outputs.output_03.resolution,
                "resolution_bits": sensor.outputs.output_03.resolution_bits,
                "description": sensor.outputs.output_03.description
            }

        },

        actions={

            "init": {
                "description": sensor.actions.init.description,
                "arguments": sensor.actions.init.arguments
            },
            "capture_single": {
                "description": sensor.actions.capture_single.description,
                "arguments": sensor.actions.capture_single.arguments
            },
            "capture_doble": {
                "description": sensor.actions.capture_doble.description,
                "arguments": sensor.actions.capture_doble.arguments
            },
            "capture_triple": {
                "description": sensor.actions.capture_triple.description,
                "arguments": sensor.actions.capture_triple.arguments
            },
            "stop": {
                "description": sensor.actions.stop.description,
                "arguments": sensor.actions.stop.arguments
            },
            "status": {
                "description": sensor.actions.status.description,
                "arguments": sensor.actions.status.arguments
            }

        },

        events={

            "hardware_fault": {
                "description": sensor.events.hardware_fault.description
            },
            "value_alert": {
                "description": sensor.events.value_alert.description
            }

        },

        telemetry={

            "topic": f"sensors/{sensor.sensorId}/data",
            "format": sensor.telemetry.format
        }
    )