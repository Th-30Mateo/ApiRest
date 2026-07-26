import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich import box
from api import BASE_URL, obtener_headers

console = Console()


def menu_internaciones():
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "🏥 GESTIÓN DE INTERNACIONES",
                border_style="bright_cyan",
                style="bold white on cyan"
            )
        )

        console.print("\n[bold cyan]1.[/] Alta internación")
        console.print("[bold cyan]2.[/] Buscar internación")
        console.print("[bold cyan]3.[/] Modificar internación")
        console.print("[bold cyan]4.[/] Eliminar internación")
        console.print("[bold cyan]5.[/] Listar internaciones")
        console.print("[bold cyan]6.[/] Volver")

        opcion = Prompt.ask(
            "\n[bold yellow]Seleccione una opción[/]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="6"
        )

        if opcion == "1":
            alta_internacion()
        elif opcion == "2":
            buscar_internacion()
        elif opcion == "3":
            modificar_internacion()
        elif opcion == "4":
            eliminar_internacion()
        elif opcion == "5":
            listar_internaciones()
        elif opcion == "6":
            break

        input("\nPresione Enter para continuar...")


def alta_internacion():
    console.print("\n[bold cyan]--- ALTA DE INTERNACIÓN ---[/]")
    try:
        internacion_id = IntPrompt.ask("[bold]ID (número entero)[/]")
        paciente_id = IntPrompt.ask("[bold]ID del paciente[/]")
        medico_id = IntPrompt.ask("[bold]ID del médico[/]")
    except ValueError:
        console.print("[red]❌ Los IDs deben ser números enteros.[/]")
        return

    fecha_ingreso = Prompt.ask("[bold]Fecha ingreso (YYYY-MM-DD)[/]")
    diagnostico = Prompt.ask("[bold]Diagnóstico[/]")
    habitacion = IntPrompt.ask("[bold]Número de habitación[/]")
    estado = Prompt.ask("[bold]Estado[/]")

    data = {
        "id": internacion_id,
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "fecha_ingreso": fecha_ingreso,
        "diagnostico": diagnostico,
        "habitacion": habitacion,
        "estado": estado
    }

    with console.status("[bold green]Registrando internación...[/]"):
        try:
            response = requests.post(
                f"{BASE_URL}/internaciones",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 201:
        console.print("[green]✅ Internación registrada correctamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def listar_internaciones():
    console.print("\n[bold cyan]--- LISTADO DE INTERNACIONES ---[/]")
    with console.status("[bold green]Cargando internaciones...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/internaciones",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        internaciones = response.json()
        if not internaciones:
            console.print("[yellow]⚠️ No hay internaciones registradas.[/]")
        else:
            tabla = Table(
                title="📋 Lista de Internaciones",
                box=box.ROUNDED,
                style="bright_cyan",
                header_style="bold cyan"
            )
            tabla.add_column("ID", style="cyan", justify="center")
            tabla.add_column("Paciente ID", style="yellow")
            tabla.add_column("Médico ID", style="yellow")
            tabla.add_column("Fecha Ingreso", style="white")
            tabla.add_column("Diagnóstico", style="green")
            tabla.add_column("Estado", style="magenta")
            for i in internaciones:
                tabla.add_row(
                    str(i["id"]),
                    str(i["paciente_id"]),
                    str(i["medico_id"]),
                    i["fecha_ingreso"],
                    i["diagnostico"],
                    i["estado"]
                )
            console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def buscar_internacion():
    try:
        internacion_id = IntPrompt.ask("\n[bold]ID de la internación a buscar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Buscando internación {internacion_id}...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/internaciones/{internacion_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        i = response.json()
        tabla = Table(
            title=f"🏥 Internación ID {i['id']}",
            box=box.SIMPLE,
            show_header=False,
            style="bright_white"
        )
        tabla.add_row("[bold]Paciente ID[/]", str(i['paciente_id']))
        tabla.add_row("[bold]Médico ID[/]", str(i['medico_id']))
        tabla.add_row("[bold]Fecha ingreso[/]", i['fecha_ingreso'])
        tabla.add_row("[bold]Diagnóstico[/]", i['diagnostico'])
        tabla.add_row("[bold]Habitación[/]", str(i['habitacion']))
        tabla.add_row("[bold]Estado[/]", i['estado'])
        console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


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
    diagnostico = Prompt.ask(f"Diagnóstico ([cyan]{actual['diagnostico']}[/])", default=actual['diagnostico'])
    habitacion = Prompt.ask(f"Habitación ([cyan]{actual['habitacion']}[/])", default=str(actual['habitacion']))
    estado = Prompt.ask(f"Estado ([cyan]{actual['estado']}[/])", default=actual['estado'])

    data = {
        "id": internacion_id,
        "paciente_id": int(paciente_id),
        "medico_id": int(medico_id),
        "fecha_ingreso": fecha_ingreso,
        "diagnostico": diagnostico,
        "habitacion": int(habitacion),
        "estado": estado
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


def eliminar_internacion():
    try:
        internacion_id = IntPrompt.ask("\n[bold]ID de la internación a eliminar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    if not Confirm.ask(f"[bold red]¿Eliminar internación con ID {internacion_id}?[/]"):
        console.print("[yellow]Operación cancelada.[/]")
        return

    with console.status(f"[bold red]Eliminando internación {internacion_id}...[/]"):
        try:
            response = requests.delete(
                f"{BASE_URL}/internaciones/{internacion_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Internación eliminada correctamente.[/]")
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")