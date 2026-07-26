import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from rich import box
from api import BASE_URL, obtener_headers

console = Console(force_terminal=True)


def menu_pacientes():
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "👤 GESTIÓN DE PACIENTES",
                border_style="bright_green",
                style="bold white on green"
            )
        )

        console.print("\n[bold cyan]1.[/] Alta paciente")
        console.print("[bold cyan]2.[/] Buscar paciente")
        console.print("[bold cyan]3.[/] Modificar paciente")
        console.print("[bold cyan]4.[/] Eliminar paciente")
        console.print("[bold cyan]5.[/] Listar pacientes")
        console.print("[bold cyan]6.[/] Volver")

        opcion = Prompt.ask(
            "\n[bold yellow]Seleccione una opción[/]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="6"
        )

        if opcion == "1":
            alta_paciente()
        elif opcion == "2":
            buscar_paciente()
        elif opcion == "3":
            modificar_paciente()
        elif opcion == "4":
            eliminar_paciente()
        elif opcion == "5":
            listar_pacientes()
        elif opcion == "6":
            break

        input("\nPresione Enter para continuar...")


def alta_paciente():
    console.print("\n[bold cyan]--- ALTA DE PACIENTE ---[/]")
    try:
        paciente_id = IntPrompt.ask("[bold]ID (número entero)[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    nombre = Prompt.ask("[bold]Nombre[/]")
    apellido = Prompt.ask("[bold]Apellido[/]")
    dni = Prompt.ask("[bold]DNI[/]")
    edad = IntPrompt.ask("[bold]Edad (número entero)[/]")          # <--- CAMBIADO
    telefono = Prompt.ask("[bold]Teléfono[/]")
    obra_social = Prompt.ask("[bold]Obra social[/]")

    data = {
        "id": paciente_id,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "edad": edad,                                             # <--- CAMBIADO
        "telefono": telefono,
        "obra_social": obra_social
    }

    with console.status("[bold green]Registrando paciente...[/]"):
        try:
            response = requests.post(
                f"{BASE_URL}/pacientes",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 201:
        console.print("[green]✅ Paciente creado exitosamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def listar_pacientes():
    console.print("\n[bold cyan]--- LISTADO DE PACIENTES ---[/]")
    with console.status("[bold green]Cargando pacientes...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/pacientes",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        pacientes = response.json()
        if not pacientes:
            console.print("[yellow]⚠️ No hay pacientes registrados.[/]")
        else:
            tabla = Table(
                title="📋 Lista de Pacientes",
                box=box.ROUNDED,
                style="bright_cyan",
                header_style="bold cyan"
            )
            tabla.add_column("ID", style="cyan", justify="center")
            tabla.add_column("Apellido", style="green")
            tabla.add_column("Nombre", style="green")
            tabla.add_column("DNI", style="yellow")
            tabla.add_column("Edad", style="white")               # <--- CAMBIADO
            for p in pacientes:
                tabla.add_row(
                    str(p["id"]),
                    p["apellido"],
                    p["nombre"],
                    p["dni"],
                    str(p["edad"])                                # <--- CAMBIADO
                )
            console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def buscar_paciente():
    try:
        paciente_id = IntPrompt.ask("\n[bold]ID del paciente a buscar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Buscando paciente {paciente_id}...[/]"):
        try:
            response = requests.get(
                f"{BASE_URL}/pacientes/{paciente_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        p = response.json()
        tabla = Table(
            title=f"👤 Paciente ID {p['id']}",
            box=box.SIMPLE,
            show_header=False,
            style="bright_white"
        )
        tabla.add_row("[bold]Nombre[/]", f"{p['nombre']} {p['apellido']}")
        tabla.add_row("[bold]DNI[/]", p['dni'])
        tabla.add_row("[bold]Edad[/]", str(p['edad']))           # <--- CAMBIADO
        tabla.add_row("[bold]Teléfono[/]", p['telefono'])
        tabla.add_row("[bold]Obra social[/]", p['obra_social'])
        console.print(tabla)
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def modificar_paciente():
    try:
        paciente_id = IntPrompt.ask("\n[bold]ID del paciente a modificar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    with console.status(f"[bold green]Obteniendo datos de paciente {paciente_id}...[/]"):
        try:
            response_get = requests.get(
                f"{BASE_URL}/pacientes/{paciente_id}",
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
    dni = Prompt.ask(f"DNI ([cyan]{actual['dni']}[/])", default=actual['dni'])
    edad = IntPrompt.ask(f"Edad ([cyan]{actual['edad']}[/])", default=actual['edad'])   # <--- CAMBIADO
    telefono = Prompt.ask(f"Teléfono ([cyan]{actual['telefono']}[/])", default=actual['telefono'])
    obra_social = Prompt.ask(f"Obra social ([cyan]{actual['obra_social']}[/])", default=actual['obra_social'])

    data = {
        "id": paciente_id,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "edad": edad,                                         # <--- CAMBIADO
        "telefono": telefono,
        "obra_social": obra_social
    }

    with console.status("[bold green]Actualizando paciente...[/]"):
        try:
            response = requests.put(
                f"{BASE_URL}/pacientes/{paciente_id}",
                json=data,
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Paciente actualizado correctamente.[/]")
        console.print(response.json())
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")


def eliminar_paciente():
    try:
        paciente_id = IntPrompt.ask("\n[bold]ID del paciente a eliminar[/]")
    except ValueError:
        console.print("[red]❌ El ID debe ser un número entero.[/]")
        return

    if not Confirm.ask(f"[bold red]¿Eliminar paciente con ID {paciente_id}?[/]"):
        console.print("[yellow]Operación cancelada.[/]")
        return

    with console.status(f"[bold red]Eliminando paciente {paciente_id}...[/]"):
        try:
            response = requests.delete(
                f"{BASE_URL}/pacientes/{paciente_id}",
                headers=obtener_headers()
            )
        except requests.exceptions.ConnectionError:
            console.print("[red]❌ Error de conexión con el servidor.[/]")
            return

    if response.status_code == 200:
        console.print("[green]✅ Paciente eliminado correctamente.[/]")
    else:
        console.print(f"[red]❌ Error {response.status_code}: {response.text}[/]")