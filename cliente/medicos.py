import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich import box
from api import BASE_URL, obtener_headers

console = Console()


def menu_medicos():
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "👨‍⚕️ GESTIÓN DE MÉDICOS",
                border_style="bright_magenta",
                style="bold white on magenta"
            )
        )

        console.print("\n[bold cyan]1.[/] Alta médico")
        console.print("[bold cyan]2.[/] Buscar médico")
        console.print("[bold cyan]3.[/] Modificar médico")
        console.print("[bold cyan]4.[/] Eliminar médico")
        console.print("[bold cyan]5.[/] Listar médicos")
        console.print("[bold cyan]6.[/] Volver")

        opcion = Prompt.ask(
            "\n[bold yellow]Seleccione una opción[/]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="6"
        )

        if opcion == "1":
            alta_medico()
        elif opcion == "2":
            buscar_medico()
        elif opcion == "3":
            modificar_medico()
        elif opcion == "4":
            eliminar_medico()
        elif opcion == "5":
            listar_medicos()
        elif opcion == "6":
            break

        input("\nPresione Enter para continuar...")


def alta_medico():
    console.print("\n[bold cyan]--- ALTA DE MÉDICO ---[/]")
    try:
        medico_id = IntPrompt.ask("[bold]ID (número entero)[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    nombre = Prompt.ask("[bold]Nombre[/]")
    apellido = Prompt.ask("[bold]Apellido[/]")
    especialidad = Prompt.ask("[bold]Especialidad[/]")
    matricula = Prompt.ask("[bold]Matrícula[/]")
    telefono = Prompt.ask("[bold]Teléfono[/]")

    data = {
        "id": medico_id,
        "nombre": nombre,
        "apellido": apellido,
        "especialidad": especialidad,
        "matricula": matricula,
        "telefono": telefono
    }

    with console.status("[bold green]Registrando médico...[/]"):
        try:
            response = requests.post(
                f"{BASE_URL}/medicos",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 201:
        console.print("[green]✅ Médico creado exitosamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def listar_medicos():
    console.print("\n[bold cyan]--- LISTADO DE MÉDICOS ---[/]")
    with console.status("[bold green]Cargando médicos...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/medicos",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        medicos = response.json()
        if not medicos:
            console.print("[yellow]⚠️ No hay médicos registrados.[/]")
        else:
            tabla = Table(
                title="📋 Lista de Médicos",
                box=box.ROUNDED,
                style="bright_magenta",
                header_style="bold magenta"
            )
            tabla.add_column("ID", style="cyan", justify="center")
            tabla.add_column("Apellido", style="green")
            tabla.add_column("Nombre", style="green")
            tabla.add_column("Especialidad", style="yellow")
            tabla.add_column("Matrícula", style="white")
            for m in medicos:
                tabla.add_row(
                    str(m["id"]),
                    m["apellido"],
                    m["nombre"],
                    m["especialidad"],
                    m["matricula"]
                )
            console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def buscar_medico():
    try:
        medico_id = IntPrompt.ask("\n[bold]ID del médico a buscar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Buscando médico {medico_id}...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/medicos/{medico_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        m = response.json()
        tabla = Table(
            title=f"👨‍⚕️ Médico ID {m['id']}",
            box=box.SIMPLE,
            show_header=False,
            style="bright_white"
        )
        tabla.add_row("[bold]Nombre[/]", f"{m['nombre']} {m['apellido']}")
        tabla.add_row("[bold]Especialidad[/]", m['especialidad'])
        tabla.add_row("[bold]Matrícula[/]", m['matricula'])
        tabla.add_row("[bold]Teléfono[/]", m['telefono'])
        console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def modificar_medico():
    try:
        medico_id = IntPrompt.ask("\n[bold]ID del médico a modificar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Obteniendo datos de médico {medico_id}...[/]"):
        try:
            response_get = requests.get(
                f"{BASE_URL}/medicos/{medico_id}",
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

    nombre = Prompt.ask(f"Nombre ([cyan]{actual['nombre']}[/])", default=actual['nombre'])
    apellido = Prompt.ask(f"Apellido ([cyan]{actual['apellido']}[/])", default=actual['apellido'])
    especialidad = Prompt.ask(f"Especialidad ([cyan]{actual['especialidad']}[/])", default=actual['especialidad'])
    matricula = Prompt.ask(f"Matrícula ([cyan]{actual['matricula']}[/])", default=actual['matricula'])
    telefono = Prompt.ask(f"Teléfono ([cyan]{actual['telefono']}[/])", default=actual['telefono'])

    data = {
        "id": medico_id,
        "nombre": nombre,
        "apellido": apellido,
        "especialidad": especialidad,
        "matricula": matricula,
        "telefono": telefono
    }

    with console.status("[bold green]Actualizando médico...[/]"):
        try:
            response = requests.put(
                f"{BASE_URL}/medicos/{medico_id}",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Médico actualizado correctamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def eliminar_medico():
    try:
        medico_id = IntPrompt.ask("\n[bold]ID del médico a eliminar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    if not Confirm.ask(f"[bold red]¿Eliminar médico con ID {medico_id}?[/]"):
        console.print("[yellow]Operación cancelada.[/]")
        return

    with console.status(f"[bold red]Eliminando médico {medico_id}...[/]"):
        try:
            response = requests.delete(
                f"{BASE_URL}/medicos/{medico_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Médico eliminado correctamente.[/]")
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")