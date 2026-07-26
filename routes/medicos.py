from fastapi import APIRouter, Depends, HTTPException
from models import Medico
from auth import verificar_token
from database import cargar_datos, guardar_datos, MEDICOS_FILE

router = APIRouter(
    prefix="/medicos",
    tags=["Médicos"]
)

@router.post("", status_code=201)
def crear_medico(medico: Medico, usuario: str = Depends(verificar_token)):
    medicos = cargar_datos(MEDICOS_FILE)
    if any(m["id"] == medico.id for m in medicos):
        raise HTTPException(400, "Ya existe un médico con ese ID.")
    medicos.append(medico.model_dump())
    guardar_datos(MEDICOS_FILE, medicos)
    return {"mensaje": "Médico creado", "medico": medico}

@router.get("")
def listar_medicos():
    return cargar_datos(MEDICOS_FILE)

@router.get("/{medico_id}")
def buscar_medico(medico_id: int):
    medicos = cargar_datos(MEDICOS_FILE)
    m = next((m for m in medicos if m["id"] == medico_id), None)
    if not m:
        raise HTTPException(404, "Médico no encontrado.")
    return m

@router.put("/{medico_id}")
def modificar_medico(medico_id: int, medico_actualizado: Medico, usuario: str = Depends(verificar_token)):
    medicos = cargar_datos(MEDICOS_FILE)
    for i, m in enumerate(medicos):
        if m["id"] == medico_id:
            medicos[i] = medico_actualizado.model_dump()
            guardar_datos(MEDICOS_FILE, medicos)
            return {"mensaje": "Médico actualizado", "medico": medico_actualizado}
    raise HTTPException(404, "Médico no encontrado.")

@router.delete("/{medico_id}")
def eliminar_medico(medico_id: int, usuario: str = Depends(verificar_token)):
    medicos = cargar_datos(MEDICOS_FILE)
    nuevos = [m for m in medicos if m["id"] != medico_id]
    if len(nuevos) == len(medicos):
        raise HTTPException(404, "Médico no encontrado.")
    guardar_datos(MEDICOS_FILE, nuevos)
    return {"mensaje": "Médico eliminado"}