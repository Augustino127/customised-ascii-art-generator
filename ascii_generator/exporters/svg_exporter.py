"""
Exporteur SVG pour ASCII art.
"""

import svgwrite
from typing import Optional


class SVGExporter:
    """Exporte l'ASCII art en format SVG vectoriel."""

    def __init__(
        self,
        char_width: float = 7.2,
        char_height: float = 14.4,
        font_family: str = "Courier New, monospace",
        font_size: int = 12,
    ):
        """
        Initialise l'exporteur SVG.

        Args:
            char_width: Largeur d'un caractère en pixels
            char_height: Hauteur d'un caractère en pixels
            font_family: Police de caractères
            font_size: Taille de la police
        """
        self.char_width = char_width
        self.char_height = char_height
        self.font_family = font_family
        self.font_size = font_size

    def export(
        self,
        ascii_art: str,
        output_path: str,
        background_color: str = "#000000",
        text_color: str = "#00ff00",
    ):
        """
        Exporte l'ASCII art en fichier SVG.

        Args:
            ascii_art: Chaîne ASCII art
            output_path: Chemin du fichier de sortie
            background_color: Couleur de fond
            text_color: Couleur du texte
        """
        lines = ascii_art.split("\n")
        max_width = max(len(line) for line in lines) if lines else 0
        height = len(lines)

        # Dimensions du SVG
        svg_width = max_width * self.char_width
        svg_height = height * self.char_height

        # Création du SVG
        dwg = svgwrite.Drawing(
            output_path, size=(f"{svg_width}px", f"{svg_height}px"), profile="full"
        )

        # Fond
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=("100%", "100%"),
                fill=background_color,
            )
        )

        # Ajout du texte ligne par ligne
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char.strip():  # Ignore les espaces
                    dwg.add(
                        dwg.text(
                            char,
                            insert=(
                                x * self.char_width,
                                (y + 1) * self.char_height - 2,
                            ),
                            fill=text_color,
                            font_family=self.font_family,
                            font_size=f"{self.font_size}px",
                        )
                    )

        dwg.save()

    def export_with_rgb(
        self,
        pixels: list,
        width: int,
        height: int,
        output_path: str,
        background_color: str = "#000000",
    ):
        """
        Exporte l'ASCII art coloré (RGB) en SVG.

        Args:
            pixels: Liste de tuples (x, y, char, r, g, b)
            width: Largeur en caractères
            height: Hauteur en caractères
            output_path: Chemin du fichier de sortie
            background_color: Couleur de fond
        """
        svg_width = width * self.char_width
        svg_height = height * self.char_height

        dwg = svgwrite.Drawing(
            output_path, size=(f"{svg_width}px", f"{svg_height}px"), profile="full"
        )

        # Fond
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=("100%", "100%"),
                fill=background_color,
            )
        )

        # Ajout des caractères colorés
        for x, y, char, r, g, b in pixels:
            if char.strip():
                color = f"rgb({r},{g},{b})"
                dwg.add(
                    dwg.text(
                        char,
                        insert=(
                            x * self.char_width,
                            (y + 1) * self.char_height - 2,
                        ),
                        fill=color,
                        font_family=self.font_family,
                        font_size=f"{self.font_size}px",
                    )
                )

        dwg.save()

    def export_with_effects(
        self,
        ascii_art: str,
        output_path: str,
        background_color: str = "#000000",
        text_color: str = "#00ff00",
        glow: bool = True,
        shadow: bool = True,
    ):
        """
        Exporte l'ASCII art avec effets SVG (glow, ombre, etc.).

        Args:
            ascii_art: Chaîne ASCII art
            output_path: Chemin du fichier de sortie
            background_color: Couleur de fond
            text_color: Couleur du texte
            glow: Ajouter effet de glow
            shadow: Ajouter une ombre
        """
        lines = ascii_art.split("\n")
        max_width = max(len(line) for line in lines) if lines else 0
        height = len(lines)

        svg_width = max_width * self.char_width
        svg_height = height * self.char_height

        dwg = svgwrite.Drawing(
            output_path, size=(f"{svg_width}px", f"{svg_height}px"), profile="full"
        )

        # Fond
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=("100%", "100%"),
                fill=background_color,
            )
        )

        # Définition des filtres
        if glow:
            glow_filter = dwg.defs.add(dwg.filter(id="glow"))
            glow_filter.feGaussianBlur(in_="SourceGraphic", stdDeviation="2")
            glow_filter.feComponentTransfer().feFuncA(type="linear", slope="3")

        if shadow:
            shadow_filter = dwg.defs.add(dwg.filter(id="shadow"))
            shadow_filter.feGaussianBlur(in_="SourceAlpha", stdDeviation="2")
            shadow_filter.feOffset(dx="2", dy="2", result="offsetblur")
            shadow_filter.feComponentTransfer().feFuncA(type="linear", slope="0.5")

        # Groupe pour le texte
        text_group = dwg.g()

        # Ajout du texte
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char.strip():
                    text_elem = dwg.text(
                        char,
                        insert=(
                            x * self.char_width,
                            (y + 1) * self.char_height - 2,
                        ),
                        fill=text_color,
                        font_family=self.font_family,
                        font_size=f"{self.font_size}px",
                    )

                    if glow:
                        text_elem["filter"] = "url(#glow)"
                    if shadow:
                        text_elem["filter"] = "url(#shadow)"

                    text_group.add(text_elem)

        dwg.add(text_group)
        dwg.save()
