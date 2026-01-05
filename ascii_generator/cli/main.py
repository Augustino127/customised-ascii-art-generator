#!/usr/bin/env python3
"""
CLI principale pour le générateur ASCII art.
"""

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from pathlib import Path
from ascii_generator.core import ImageToASCII, TextToASCII, AnimationToASCII
from ascii_generator.palettes import CharacterPalettes, ArtisticStyles
from ascii_generator.effects import ArtisticEffects
from ascii_generator.exporters import HTMLExporter, SVGExporter
from PIL import Image

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🎨 Générateur ASCII Art Personnalisé

    Un générateur complet avec fonctionnalités avancées et innovations.
    """
    pass


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--width", "-w", default=100, help="Largeur en caractères")
@click.option(
    "--palette",
    "-p",
    default="STANDARD",
    help="Palette de caractères (voir --list-palettes)",
)
@click.option("--invert", "-i", is_flag=True, help="Inverser les tons")
@click.option(
    "--color",
    "-c",
    type=click.Choice(["monochrome", "ansi", "rgb"]),
    default="monochrome",
    help="Mode de couleur",
)
@click.option("--contrast", default=1.0, help="Contraste (0.5-2.0)")
@click.option("--brightness", default=0, help="Luminosité (-100 à 100)")
@click.option(
    "--algorithm",
    type=click.Choice(["luminosity", "average", "lightness"]),
    default="luminosity",
    help="Algorithme de conversion",
)
@click.option("--output", "-o", help="Fichier de sortie (défaut: stdout)")
@click.option("--edge-detect", is_flag=True, help="Détection de contours")
@click.option(
    "--dithering",
    type=click.Choice(["floyd", "bayer"]),
    help="Appliquer dithering",
)
@click.option("--export-html", help="Exporter en HTML")
@click.option("--export-svg", help="Exporter en SVG")
def image(
    image_path,
    width,
    palette,
    invert,
    color,
    contrast,
    brightness,
    algorithm,
    output,
    edge_detect,
    dithering,
    export_html,
    export_svg,
):
    """Convertit une IMAGE en ASCII art."""
    try:
        # Récupération de la palette
        palette_chars = CharacterPalettes.get_palette(palette)

        # Création du convertisseur
        converter = ImageToASCII(
            palette=palette_chars,
            width=width,
            color_mode=color,
            invert=invert,
            contrast=contrast,
            brightness=brightness,
            algorithm=algorithm,
        )

        # Conversion avec options
        if edge_detect:
            console.print("[cyan]🔍 Détection de contours activée[/cyan]")
            ascii_art = converter.convert_with_edge_detection(image_path)
        elif dithering:
            console.print(f"[cyan]🎨 Dithering {dithering} appliqué[/cyan]")
            ascii_art = converter.convert_with_dithering(image_path, method=dithering)
        else:
            ascii_art = converter.convert(image_path)

        # Sortie
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(ascii_art)
            console.print(f"[green]✓ Sauvegardé dans {output}[/green]")
        else:
            print(ascii_art)

        # Exports supplémentaires
        if export_html:
            exporter = HTMLExporter()
            exporter.export(ascii_art, export_html)
            console.print(f"[green]✓ Exporté en HTML: {export_html}[/green]")

        if export_svg:
            exporter = SVGExporter()
            exporter.export(ascii_art, export_svg)
            console.print(f"[green]✓ Exporté en SVG: {export_svg}[/green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.argument("text")
@click.option(
    "--font", "-f", default="standard", help="Police (voir --list-fonts)"
)
@click.option("--width", "-w", type=int, help="Largeur maximale")
@click.option("--color", "-c", help="Couleur ANSI (red, green, cyan, etc.)")
@click.option("--banner", "-b", is_flag=True, help="Créer une bannière avec bordures")
@click.option("--gradient", is_flag=True, help="Appliquer un gradient de couleurs")
@click.option("--shadow", is_flag=True, help="Ajouter une ombre")
@click.option("--output", "-o", help="Fichier de sortie")
def text(text, font, width, color, banner, gradient, shadow, output):
    """Convertit du TEXTE en ASCII art."""
    try:
        converter = TextToASCII(font=font, width=width)

        if shadow:
            ascii_art = converter.create_shadow(text)
        elif gradient:
            # Gradient cyan -> magenta
            ascii_art = converter.create_gradient(
                text, start_color=(0, 255, 255), end_color=(255, 0, 255)
            )
        elif banner:
            ascii_art = converter.create_banner(text)
        else:
            ascii_art = converter.convert(text, color=color)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(ascii_art)
            console.print(f"[green]✓ Sauvegardé dans {output}[/green]")
        else:
            print(ascii_art)

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("--width", "-w", default=80, help="Largeur en caractères")
@click.option("--fps", type=int, help="Images par seconde")
@click.option("--max-frames", type=int, help="Nombre maximum de frames")
@click.option("--play", is_flag=True, help="Jouer l'animation")
@click.option("--loop", is_flag=True, help="Boucler l'animation")
@click.option("--save", "-s", help="Sauvegarder dans un fichier")
@click.option("--export-html", help="Exporter en HTML animé")
@click.option("--skip-frames", default=1, help="Sauter N frames (pour vidéos)")
def animate(input_path, width, fps, max_frames, play, loop, save, export_html, skip_frames):
    """Convertit un GIF ou une VIDÉO en animation ASCII."""
    try:
        converter = AnimationToASCII(width=width, fps=fps)

        # Détection du type de fichier
        path = Path(input_path)
        if path.suffix.lower() in [".gif"]:
            console.print("[cyan]🎬 Conversion du GIF...[/cyan]")
            frames = converter.convert_gif(input_path, max_frames=max_frames)
        elif path.suffix.lower() in [".mp4", ".avi", ".mov", ".mkv"]:
            console.print("[cyan]🎬 Conversion de la vidéo...[/cyan]")
            frames = converter.convert_video(
                input_path, max_frames=max_frames, skip_frames=skip_frames
            )
        else:
            console.print("[red]✗ Format non supporté[/red]")
            raise click.Abort()

        console.print(f"[green]✓ {len(frames)} frames converties[/green]")

        # Sauvegarde
        if save:
            converter.save_animation(frames, save)
            console.print(f"[green]✓ Animation sauvegardée: {save}[/green]")

        # Export HTML
        if export_html:
            converter.export_to_html(frames, export_html, fps=fps or 10)
            console.print(f"[green]✓ Exporté en HTML: {export_html}[/green]")

        # Lecture
        if play:
            console.print("[yellow]▶ Lecture de l'animation (Ctrl+C pour arrêter)[/yellow]")
            converter.play_animation(frames, fps=fps, loop=loop)

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")
        raise click.Abort()


@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option(
    "--effect",
    type=click.Choice([
        "stipple", "halftone", "glow", "vintage",
        "glitch", "cyberpunk", "3d"
    ]),
    required=True,
    help="Effet à appliquer",
)
@click.option("--output", "-o", required=True, help="Image de sortie")
@click.option("--width", "-w", default=100, help="Largeur pour conversion ASCII")
def effect(image_path, effect, output, width):
    """Applique des EFFETS artistiques avancés."""
    try:
        image = Image.open(image_path)
        effects = ArtisticEffects()

        console.print(f"[cyan]🎨 Application de l'effet '{effect}'...[/cyan]")

        if effect == "stipple":
            processed = effects.apply_stippling(image, density=2000)
        elif effect == "halftone":
            processed = effects.apply_halftone(image, dot_size=5)
        elif effect == "glow":
            processed = effects.apply_edge_glow(image, intensity=2.0)
        elif effect == "vintage":
            processed = effects.apply_vintage_effect(image)
        elif effect == "glitch":
            processed = effects.apply_glitch_effect(image, intensity=15)
        elif effect == "cyberpunk":
            processed = effects.apply_cyberpunk_effect(image)
        elif effect == "3d":
            processed = effects.apply_3d_effect(image, depth=8)

        # Sauvegarde de l'image avec effet
        processed.save(output)
        console.print(f"[green]✓ Image avec effet sauvegardée: {output}[/green]")

        # Optionnel: conversion en ASCII
        converter = ImageToASCII(width=width)
        ascii_art = converter.convert(image=processed)

        ascii_output = output.replace(Path(output).suffix, ".txt")
        with open(ascii_output, "w", encoding="utf-8") as f:
            f.write(ascii_art)
        console.print(f"[green]✓ ASCII art sauvegardé: {ascii_output}[/green]")

    except Exception as e:
        console.print(f"[red]✗ Erreur: {e}[/red]")
        raise click.Abort()


@cli.command()
def list_palettes():
    """Liste toutes les palettes disponibles."""
    table = Table(title="🎨 Palettes de Caractères Disponibles")
    table.add_column("Nom", style="cyan")
    table.add_column("Aperçu", style="green")

    palettes = CharacterPalettes.list_palettes()
    for palette_name in palettes:
        palette = CharacterPalettes.get_palette(palette_name)
        preview = palette[:30] + "..." if len(palette) > 30 else palette
        table.add_row(palette_name, preview)

    console.print(table)


@cli.command()
@click.option("--max", "-m", default=20, help="Nombre maximum de polices à afficher")
def list_fonts(max):
    """Liste les polices disponibles."""
    console.print(f"[cyan]📝 Polices disponibles (total: {len(TextToASCII.list_fonts())})[/cyan]\n")

    fonts = TextToASCII.list_fonts()[:max]
    for i, font in enumerate(fonts, 1):
        console.print(f"{i:3}. {font}")

    if len(TextToASCII.list_fonts()) > max:
        console.print(f"\n[dim]... et {len(TextToASCII.list_fonts()) - max} autres[/dim]")


@cli.command()
@click.option("--text", "-t", default="Demo", help="Texte à afficher")
@click.option("--max-fonts", default=5, help="Nombre de polices à prévisualiser")
def preview_fonts(text, max_fonts):
    """Prévisualise plusieurs polices."""
    preview = TextToASCII.preview_fonts(text=text, max_fonts=max_fonts)
    print(preview)


@cli.command()
def styles():
    """Affiche les styles artistiques prédéfinis."""
    table = Table(title="🎭 Styles Artistiques Prédéfinis")
    table.add_column("Style", style="cyan")
    table.add_column("Palette", style="green")
    table.add_column("Contraste", style="yellow")

    for style_name in dir(ArtisticStyles):
        if not style_name.startswith("_"):
            style = getattr(ArtisticStyles, style_name)
            if isinstance(style, dict):
                palette_name = (
                    style.get("palette", "")[:20] + "..."
                    if len(style.get("palette", "")) > 20
                    else style.get("palette", "")
                )
                table.add_row(
                    style_name,
                    palette_name,
                    str(style.get("contrast", 1.0)),
                )

    console.print(table)


@cli.command()
def interactive():
    """Mode interactif avec menu."""
    from ascii_generator.cli.interactive import run_interactive_mode
    run_interactive_mode()


if __name__ == "__main__":
    cli()
