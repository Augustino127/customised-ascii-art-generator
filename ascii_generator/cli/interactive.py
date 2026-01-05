"""
Mode interactif pour le générateur ASCII art.
"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from ascii_generator.core import ImageToASCII, TextToASCII
from ascii_generator.palettes import CharacterPalettes
from pathlib import Path

console = Console()


def run_interactive_mode():
    """Lance le mode interactif."""
    console.print(
        Panel.fit(
            "[bold cyan]🎨 Générateur ASCII Art - Mode Interactif[/bold cyan]\n"
            "Tapez 'help' pour voir les commandes disponibles\n"
            "Tapez 'exit' pour quitter",
            border_style="cyan",
        )
    )

    commands = [
        "image",
        "text",
        "animate",
        "palettes",
        "fonts",
        "help",
        "exit",
    ]
    completer = WordCompleter(commands, ignore_case=True)

    # État de la session
    session_state = {
        "last_converter": None,
        "last_output": None,
    }

    while True:
        try:
            user_input = prompt(
                "\n[ASCII] > ", completer=completer
            ).strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command == "exit":
                console.print("[yellow]👋 Au revoir![/yellow]")
                break

            elif command == "help":
                show_help()

            elif command == "image":
                handle_image_command(parts, session_state)

            elif command == "text":
                handle_text_command(parts, session_state)

            elif command == "palettes":
                list_palettes()

            elif command == "fonts":
                list_fonts()

            elif command == "clear":
                console.clear()

            else:
                console.print(f"[red]Commande inconnue: {command}[/red]")
                console.print("Tapez 'help' pour voir les commandes disponibles")

        except KeyboardInterrupt:
            console.print("\n[yellow]Utilisez 'exit' pour quitter[/yellow]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")


def show_help():
    """Affiche l'aide."""
    help_text = """
# Commandes Disponibles

## Conversion d'Images
```
image <chemin> [--width N] [--palette NOM] [--color MODE]
```
Exemple: `image photo.jpg --width 80 --palette DETAILED`

## Conversion de Texte
```
text <texte> [--font NOM] [--color COULEUR]
```
Exemple: `text "Hello World" --font banner --color cyan`

## Informations
- `palettes` - Liste les palettes disponibles
- `fonts` - Liste les polices disponibles
- `help` - Affiche cette aide
- `clear` - Efface l'écran
- `exit` - Quitte le mode interactif

## Options Communes
- `--width N` - Largeur en caractères
- `--palette NOM` - Palette de caractères
- `--color MODE` - Mode de couleur (monochrome, ansi, rgb)
    """
    console.print(Markdown(help_text))


def handle_image_command(parts, session_state):
    """Traite la commande image."""
    if len(parts) < 2:
        console.print("[red]Usage: image <chemin> [options][/red]")
        return

    image_path = parts[1]

    if not Path(image_path).exists():
        console.print(f"[red]Fichier introuvable: {image_path}[/red]")
        return

    # Parse des options
    width = 80
    palette = "STANDARD"
    color_mode = "monochrome"

    i = 2
    while i < len(parts):
        if parts[i] == "--width" and i + 1 < len(parts):
            width = int(parts[i + 1])
            i += 2
        elif parts[i] == "--palette" and i + 1 < len(parts):
            palette = parts[i + 1]
            i += 2
        elif parts[i] == "--color" and i + 1 < len(parts):
            color_mode = parts[i + 1]
            i += 2
        else:
            i += 1

    try:
        console.print(f"[cyan]🖼️  Conversion de {image_path}...[/cyan]")

        palette_chars = CharacterPalettes.get_palette(palette)
        converter = ImageToASCII(
            palette=palette_chars, width=width, color_mode=color_mode
        )

        ascii_art = converter.convert(image_path)
        session_state["last_converter"] = converter
        session_state["last_output"] = ascii_art

        print("\n" + ascii_art)

        console.print(
            f"\n[green]✓ Conversion terminée ({width} caractères de large)[/green]"
        )

        # Proposer de sauvegarder
        save = prompt("Sauvegarder dans un fichier? (o/N): ").strip().lower()
        if save == "o":
            filename = prompt("Nom du fichier: ").strip()
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(ascii_art)
                console.print(f"[green]✓ Sauvegardé dans {filename}[/green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")


def handle_text_command(parts, session_state):
    """Traite la commande text."""
    if len(parts) < 2:
        console.print("[red]Usage: text <texte> [options][/red]")
        return

    text = parts[1]

    # Parse des options
    font = "standard"
    color = None

    i = 2
    while i < len(parts):
        if parts[i] == "--font" and i + 1 < len(parts):
            font = parts[i + 1]
            i += 2
        elif parts[i] == "--color" and i + 1 < len(parts):
            color = parts[i + 1]
            i += 2
        else:
            i += 1

    try:
        console.print(f"[cyan]📝 Conversion du texte...[/cyan]")

        converter = TextToASCII(font=font)
        ascii_art = converter.convert(text, color=color)

        session_state["last_converter"] = converter
        session_state["last_output"] = ascii_art

        print("\n" + ascii_art)

        console.print(f"\n[green]✓ Conversion terminée (police: {font})[/green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")


def list_palettes():
    """Liste les palettes."""
    from rich.table import Table

    table = Table(title="🎨 Palettes Disponibles")
    table.add_column("Nom", style="cyan")
    table.add_column("Aperçu", style="green")

    palettes = CharacterPalettes.list_palettes()
    for palette_name in palettes[:15]:  # Limite pour l'affichage
        palette = CharacterPalettes.get_palette(palette_name)
        preview = palette[:30] + "..." if len(palette) > 30 else palette
        table.add_row(palette_name, preview)

    console.print(table)

    if len(palettes) > 15:
        console.print(f"[dim]... et {len(palettes) - 15} autres palettes[/dim]")


def list_fonts():
    """Liste les polices."""
    fonts = TextToASCII.list_fonts()[:20]
    console.print("[cyan]📝 Polices disponibles (20 premières):[/cyan]\n")

    for i, font in enumerate(fonts, 1):
        console.print(f"  {i:2}. {font}")

    console.print(
        f"\n[dim]Total: {len(TextToASCII.list_fonts())} polices disponibles[/dim]"
    )
