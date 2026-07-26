"""
CRUD de Internaciones
"""

from fastapi import APIRouter, Depends, HTTPException

from models import Internacion
from auth import verificar_token

from database import (
    cargar_datos,
    guardar_datos,
    INTERNACIONES_FILE,
    PACIENTES_FILE,
    MEDICOS_FILE
)

router = APIRouter(
    prefix="/internaciones",
    tags=["Internaciones"]
)



@router.post(
    "",
    status_code=201,
    summary="Registrar internación"
)
def crear_internacion(
    internacion: Internacion,
    usuario: str = Depends(verificar_token)
):

    internaciones = cargar_datos(INTERNACIONES_FILE)
    pacientes = cargar_datos(PACIENTES_FILE)
    medicos = cargar_datos(MEDICOS_FILE)

    if any(i["id"] == internacion.id for i in internaciones):
        raise HTTPException(
            status_code=400,
            detail="Ya existe una internación con ese ID."
        )

    if not any(p["id"] == internacion.paciente_id for p in pacientes):
        raise HTTPException(
            status_code=400,
            detail="El paciente no existe."
        )

    if not any(m["id"] == internacion.medico_id for m in medicos):
        raise HTTPException(
            status_code=400,
            detail="El médico no existe."
        )

    internaciones.append(internacion.model_dump())

    guardar_datos(INTERNACIONES_FILE, internaciones)

    return {
        "mensaje": "Internación registrada correctamente.",
        "internacion": internacion
    }



@router.get(
    "",
    summary="Listar internaciones"
)
def listar_internaciones():

    return cargar_datos(INTERNACIONES_FILE)



@router.get(
    "/{internacion_id}",
    summary="Buscar internación"
)
def buscar_internacion(internacion_id: int):

    internaciones = cargar_datos(INTERNACIONES_FILE)

    internacion = next(
        (i for i in internaciones if i["id"] == internacion_id),
        None
    )

    if internacion is None:
        raise HTTPException(
            status_code=404,
            detail="Internación no encontrada."
        )

    return internacion

@router.put(
    "/{internacion_id}",
    summary="Modificar internación"
)
def modificar_internacion():
    try:
        internacion_id = IntPrompt.ask("\n[bold]ID de la internación a modificar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Obteniendo datos de internación {internacion_id}...[/]"):
        try:
            response_get = requests.get(
                f"{BASE_URL}/internaciones/{internacion_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response_get.status_code != 200:
        console.print(f"[red]❌ Error: {response_get.text}[/]")
        return

    actual = response_get.json()
    console.print("\n[bold]Deje en blanco para mantener el valor actual.[/]")

    paciente_id = Prompt.ask(f"Paciente ID ([cyan]{actual['paciente_id']}[/])", default=str(actual['paciente_id']))
    medico_id = Prompt.ask(f"Médico ID ([cyan]{actual['medico_id']}[/])", default=str(actual['medico_id']))
    fecha_ingreso = Prompt.ask(f"Fecha ingreso ([cyan]{actual['fecha_ingreso']}[/])", default=actual['fecha_ingreso'])
    fecha_alta = Prompt.ask(f"Fecha alta ([cyan]{actual.get('fecha_alta', '')}[/])", default=actual.get('fecha_alta', ''))
    diagnostico = Prompt.ask(f"Diagnóstico ([cyan]{actual['diagnostico']}[/])", default=actual['diagnostico'])
    habitacion = Prompt.ask(f"Habitación ([cyan]{actual['habitacion']}[/])", default=actual['habitacion'])

    data = {
        "id": internacion_id,  # <--- AGREGADO
        "paciente_id": int(paciente_id),
        "medico_id": int(medico_id),
        "fecha_ingreso": fecha_ingreso,
        "fecha_alta": fecha_alta if fecha_alta else None,
        "diagnostico": diagnostico,
        "habitacion": habitacion
    }

    with console.status("[bold green]Actualizando internación...[/]"):
        try:
            response = requests.put(
                f"{BASE_URL}/internaciones/{internacion_id}",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Internación actualizada correctamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")
@router.delete(
    "/{internacion_id}",
    summary="Eliminar internación"
)
def eliminar_internacion(
    internacion_id: int,
    usuario: str = Depends(verificar_token)
):

    internaciones = cargar_datos(INTERNACIONES_FILE)

    nuevas = [
        i for i in internaciones
        if i["id"] != internacion_id
    ]

    if len(nuevas) == len(internaciones):
        raise HTTPException(
            status_code=404,
            detail="Internación no encontrada."
        )

    guardar_datos(INTERNACIONES_FILE, nuevas)

    return {
        "mensaje": "Internación eliminada correctamente."
    }