from fastapi import FastAPI
from routes.pacientes import router as pacientes_router
from routes.medicos import router as medicos_router
from routes.internaciones import router as internaciones_router
from auth import router as auth_router 

tags_metadata = [
    {
        "name": "Autenticación",
        "description": "Inicio de sesión y generación del Bearer Token."
    },
    {
        "name": "Pacientes",
        "description": "Administración de pacientes."
    },
    {
        "name": "Médicos",
        "description": "Administración de médicos."
    },
    {
        "name": "Internaciones",
        "description": "Administración de internaciones."
    }
]
app = FastAPI(
    title="API REST - Sistema de Gestión Hospitalaria",
    description="GRUPO 10",
    version="1.0.0",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "syntaxHighlight": False,
        "defaultModelsExpandDepth": -1
    }
)
app.include_router(auth_router)        
app.include_router(pacientes_router)
app.include_router(medicos_router)
app.include_router(internaciones_router)