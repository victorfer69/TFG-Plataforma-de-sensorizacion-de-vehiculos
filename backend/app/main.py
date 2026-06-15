from fastapi import FastAPI
from app.routes.sensor_routes import router as sensor_router
from fastapi.middleware.cors import CORSMiddleware

# Define la instancia de aplicación FastAPI
app = FastAPI(title="Sistema sensorización TFG")

# Actúa como punto de entrada al sistema
app.include_router(sensor_router)

# Configuraciones para comunicación frontend <-> backend en local
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)