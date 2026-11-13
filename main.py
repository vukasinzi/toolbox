from rich.console import Console
from core.registry import TOOLS
from core.logger import logger
from core.history import add_entry

console = Console(force_terminal=True)


def show_menu():
    console.print("\n[bold cyan]=== TOOLBOX ===[/bold cyan]")
    for key, (name, _) in TOOLS.items():
        console.print(f"\\[{key}] {name}")
    console.print("\\[0] Exit")


def run_tool(choice):
    name, func = TOOLS[choice]
    logger.info(f"Pokrenut alat: {name}")
    add_entry(name)
    try:
        func()
    except KeyboardInterrupt:
        console.print("\n[yellow]Prekinuto, vraćam se u meni.[/yellow]")
    except Exception as e:
        logger.error(f"Greška u alatu {name}: {e}", exc_info=True)
        console.print(f"[red]Alat je prijavio grešku: {e}[/red]")


def handle_choice(choice):
    """Vraća False kad korisnik želi da izađe, inače True."""
    match choice:
        case "0":
            return False
        case _ if choice in TOOLS:
            run_tool(choice)
        case _:
            console.print("[red]Nevažeći izbor.[/red]")
    return True


def main():
    logger.info("TOOLBOX pokrenut")
    try:
        running = True
        while running:
            show_menu()
            running = handle_choice(console.input("\nSelect tool > ").strip())
    except (KeyboardInterrupt, EOFError):
        pass
    console.print("Bye!")
    logger.info("TOOLBOX zatvoren")


if __name__ == "__main__":
    main()