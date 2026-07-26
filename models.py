from pydantic import BaseModel, Field, ConfigDict


# =====================================================
# MODELO DE LOGIN
# =====================================================

class Login(BaseModel):
    """Modelo utilizado para iniciar sesión."""

    usuario: str = Field(
        ...,
        min_length=3,
        description="Nombre de usuario."
    )

    password: str = Field(
        ...,
        min_length=3,
        description="Contraseña del usuario."
    )


# =====================================================
# MODELO PACIENTE
# =====================================================

class Paciente(BaseModel):
    """Representa un paciente del hospital."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "dni": "40111222",
                "nombre": "Juan",
                "apellido": "Pérez",
                "edad": 28,
                "telefono": "3875551234",
                "obra_social": "OSDE"
            }
        }
    )

    id: int = Field(
        ...,
        gt=0,
        description="Identificador único del paciente."
    )

    dni: str = Field(
        ...,
        min_length=7,
        max_length=10,
        description="Documento Nacional de Identidad."
    )

    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del paciente."
    )

    apellido: str = Field(
        ...,
        min_length=1,
        description="Apellido del paciente."
    )

    edad: int = Field(
        ...,
        gt=0,
        description="Edad del paciente (mayor que cero)."
    )

    telefono: str = Field(
        ...,
        min_length=6,
        description="Número telefónico."
    )

    obra_social: str = Field(
        ...,
        min_length=1,
        description="Obra social del paciente."
    )


# =====================================================
# MODELO MÉDICO
# =====================================================

class Medico(BaseModel):
    """Representa un médico del hospital."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "matricula": "MP12345",
                "nombre": "María",
                "apellido": "Gómez",
                "especialidad": "Cardiología",
                "telefono": "3874447788"
            }
        }
    )

    id: int = Field(
        ...,
        gt=0,
        description="Identificador único del médico."
    )

    matricula: str = Field(
        ...,
        min_length=1,
        description="Número de matrícula profesional."
    )

    nombre: str = Field(
        ...,
        min_length=1,
        description="Nombre del médico."
    )

    apellido: str = Field(
        ...,
        min_length=1,
        description="Apellido del médico."
    )

    especialidad: str = Field(
        ...,
        min_length=1,
        description="Especialidad médica."
    )

    telefono: str = Field(
        ...,
        min_length=6,
        description="Número telefónico."
    )


# =====================================================
# MODELO INTERNACIÓN
# =====================================================

class Internacion(BaseModel):
    """Representa una internación."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "paciente_id": 1,
                "medico_id": 1,
                "fecha_ingreso": "2026-07-16",
                "diagnostico": "Neumonía",
                "habitacion": 205,
                "estado": "Internado"
            }
        }
    )

    id: int = Field(
        ...,
        gt=0,
        description="Identificador único de la internación."
    )

    paciente_id: int = Field(
        ...,
        gt=0,
        description="ID del paciente."
    )

    medico_id: int = Field(
        ...,
        gt=0,
        description="ID del médico responsable."
    )

    fecha_ingreso: str = Field(
        ...,
        description="Fecha de ingreso (AAAA-MM-DD)."
    )

    diagnostico: str = Field(
        ...,
        min_length=1,
        description="Diagnóstico inicial."
    )

    habitacion: int = Field(
        ...,
        gt=0,
        description="Número de habitación."
    )

    estado: str = Field(
        ...,
        min_length=1,
        description="Estado actual de la internación."
    )