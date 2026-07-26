from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from api import login
import pacientes
import medicos
import internaciones

console = Console(force_terminal=True)


def mostrar_menu():
    """Muestra el menú principal con estilo."""
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "🏥 SISTEMA HOSPITALARIO",
                border_style="bright_blue",
                style="bold white on blue"
            )
        )

        console.print("\n[bold cyan]1.[/] Iniciar sesión")
        console.print("[bold cyan]2.[/] Gestionar pacientes")
        console.print("[bold cyan]3.[/] Gestionar médicos")
        console.print("[bold cyan]4.[/] Gestionar internaciones")
        console.print("[bold cyan]5.[/] Salir")

        opcion = Prompt.ask(
            "\n[bold yellow]Seleccione una opción[/]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )

        if opcion == "1":
            login()
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            pacientes.menu_pacientes()
        elif opcion == "3":
            medicos.menu_medicos()
        elif opcion == "4":
            internaciones.menu_internaciones()
        elif opcion == "5":
            console.print("\n[bold green]¡Hasta luego! 👋[/]")
            break


if __name__ == "__main__":
    mostrar_menu()