from fastapi import APIRouter, Depends, HTTPException
from models import Paciente
from auth import verificar_token
from database import cargar_datos, guardar_datos, PACIENTES_FILE

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

@router.post("", status_code=201)
def crear_paciente(paciente: Paciente, usuario: str = Depends(verificar_token)):
    pacientes = cargar_datos(PACIENTES_FILE)
    if any(p["id"] == paciente.id for p in pacientes):
        raise HTTPException(400, "Ya existe un paciente con ese ID.")
    pacientes.append(paciente.model_dump())
    guardar_datos(PACIENTES_FILE, pacientes)
    return {"mensaje": "Paciente creado", "paciente": paciente}

@router.get("")
def listar_pacientes():
    return cargar_datos(PACIENTES_FILE)

@router.get("/{paciente_id}")
def buscar_paciente(paciente_id: int):
    pacientes = cargar_datos(PACIENTES_FILE)
    p = next((p for p in pacientes if p["id"] == paciente_id), None)
    if not p:
        raise HTTPException(404, "Paciente no encontrado.")
    return p

@router.put("/{paciente_id}")
def modificar_paciente(paciente_id: int, paciente_actualizado: Paciente, usuario: str = Depends(verificar_token)):
    pacientes = cargar_datos(PACIENTES_FILE)
    for i, p in enumerate(pacientes):
        if p["id"] == paciente_id:
            pacientes[i] = paciente_actualizado.model_dump()
            guardar_datos(PACIENTES_FILE, pacientes)
            return {"mensaje": "Paciente actualizado", "paciente": paciente_actualizado}
    raise HTTPException(404, "Paciente no encontrado.")

@router.delete("/{paciente_id}")
def eliminar_paciente(paciente_id: int, usuario: str = Depends(verificar_token)):
    pacientes = cargar_datos(PACIENTES_FILE)
    nuevos = [p for p in pacientes if p["id"] != paciente_id]
    if len(nuevos) == len(pacientes):
        raise HTTPException(404, "Paciente no encontrado.")
    guardar_datos(PACIENTES_FILE, nuevos)
    return {"mensaje": "Paciente eliminado"}