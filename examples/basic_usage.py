#!/usr/bin/env python3
"""
Exemples d'utilisation du générateur ASCII art.
"""

from ascii_generator import ImageToASCII, TextToASCII, AnimationToASCII
from ascii_generator.palettes import CharacterPalettes, ArtisticStyles
from ascii_generator.effects import ArtisticEffects
from ascii_generator.exporters import HTMLExporter, SVGExporter
from PIL import Image, ImageDraw


def example_text_conversion():
    """Exemple de conversion de texte."""
    print("=" * 60)
    print("EXEMPLE 1: Conversion de texte")
    print("=" * 60)

    converter = TextToASCII(font="banner")

    # Texte simple
    ascii_art = converter.convert("ASCII")
    print(ascii_art)

    # Avec couleur
    colored = converter.convert("Colored", color="cyan")
    print(colored)

    # Bannière
    banner = converter.create_banner("TITLE", border_char="=", padding=2)
    print(banner)


def example_image_conversion():
    """Exemple de conversion d'image."""
    print("\n" + "=" * 60)
    print("EXEMPLE 2: Conversion d'image")
    print("=" * 60)

    # Création d'une image de test
    img = Image.new("RGB", (200, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Dessiner un cercle
    draw.ellipse([50, 25, 150, 75], fill=(0, 0, 0), outline=(0, 0, 0))

    # Conversion en ASCII
    converter = ImageToASCII(
        palette=CharacterPalettes.DETAILED,
        width=50,
        contrast=1.2
    )

    ascii_art = converter.convert(image=img)
    print(ascii_art)


def example_palettes():
    """Exemple d'utilisation des palettes."""
    print("\n" + "=" * 60)
    print("EXEMPLE 3: Différentes palettes")
    print("=" * 60)

    # Création d'une image de test simple
    img = Image.new("L", (100, 50), color=255)
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 10, 80, 40], fill=0)

    palettes_to_test = ["STANDARD", "BLOCKS", "STIPPLE", "BINARY"]

    for palette_name in palettes_to_test:
        print(f"\n--- Palette: {palette_name} ---")
        palette = CharacterPalettes.get_palette(palette_name)
        converter = ImageToASCII(palette=palette, width=30)
        ascii_art = converter.convert(image=img)
        print(ascii_art)


def example_artistic_effects():
    """Exemple d'effets artistiques."""
    print("\n" + "=" * 60)
    print("EXEMPLE 4: Effets artistiques")
    print("=" * 60)

    # Création d'une image de test avec gradient
    img = Image.new("L", (200, 100))
    pixels = img.load()

    for y in range(100):
        for x in range(200):
            pixels[x, y] = int((x / 200) * 255)

    effects = ArtisticEffects()

    # Effet stippling
    print("\n--- Stippling ---")
    stippled = effects.apply_stippling(img, density=500, size_range=(1, 3))
    converter = ImageToASCII(width=50)
    ascii_art = converter.convert(image=stippled)
    print(ascii_art[:500] + "...")  # Aperçu


def example_text_effects():
    """Exemple d'effets sur le texte."""
    print("\n" + "=" * 60)
    print("EXEMPLE 5: Effets de texte")
    print("=" * 60)

    converter = TextToASCII(font="banner")

    # Gradient
    print("\n--- Gradient ---")
    gradient = converter.create_gradient(
        "GRAD",
        start_color=(0, 255, 255),  # Cyan
        end_color=(255, 0, 255)     # Magenta
    )
    print(gradient)

    # Ombre
    print("\n--- Avec ombre ---")
    shadow = converter.create_shadow("SHADOW", shadow_offset=(2, 1))
    print(shadow)


def example_export():
    """Exemple d'export."""
    print("\n" + "=" * 60)
    print("EXEMPLE 6: Export HTML et SVG")
    print("=" * 60)

    converter = TextToASCII(font="banner")
    ascii_art = converter.convert("EXPORT")

    # Export HTML
    html_exporter = HTMLExporter(
        background_color="#000000",
        text_color="#00ff00",
        font_size=12
    )

    try:
        html_exporter.export(
            ascii_art,
            "examples/export_example.html",
            title="Exemple ASCII Art"
        )
        print("✓ Exporté en HTML: examples/export_example.html")
    except Exception as e:
        print(f"Note: {e}")

    # Export SVG
    svg_exporter = SVGExporter(font_size=12)

    try:
        svg_exporter.export(
            ascii_art,
            "examples/export_example.svg",
            background_color="#000000",
            text_color="#00ff00"
        )
        print("✓ Exporté en SVG: examples/export_example.svg")
    except Exception as e:
        print(f"Note: {e}")


def example_custom_palette():
    """Exemple de palette personnalisée."""
    print("\n" + "=" * 60)
    print("EXEMPLE 7: Palette personnalisée")
    print("=" * 60)

    # Création d'une palette personnalisée
    custom_chars = "█▓▒░ .,:;-=+*#@"
    custom_palette = CharacterPalettes.custom_palette(custom_chars)

    print(f"Palette personnalisée: {custom_palette}")

    # Test avec une image
    img = Image.new("L", (100, 50), color=255)
    draw = ImageDraw.Draw(img)

    # Dessiner des rectangles avec différentes intensités
    draw.rectangle([10, 10, 30, 40], fill=200)
    draw.rectangle([35, 10, 55, 40], fill=150)
    draw.rectangle([60, 10, 80, 40], fill=100)
    draw.rectangle([85, 10, 95, 40], fill=50)

    converter = ImageToASCII(palette=custom_palette, width=40)
    ascii_art = converter.convert(image=img)
    print(ascii_art)


def main():
    """Fonction principale."""
    print("\n🎨 EXEMPLES D'UTILISATION DU GÉNÉRATEUR ASCII ART\n")

    try:
        example_text_conversion()
        example_image_conversion()
        example_palettes()
        example_artistic_effects()
        example_text_effects()
        example_export()
        example_custom_palette()

        print("\n" + "=" * 60)
        print("✓ Tous les exemples ont été exécutés avec succès!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
