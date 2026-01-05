"""
Convertisseur de texte en ASCII art (banners, styles).
"""

import pyfiglet
from art import text2art, art
from typing import Optional, List


class TextToASCII:
    """Convertit du texte en ASCII art stylisé."""

    def __init__(self, font: str = "standard", width: Optional[int] = None):
        """
        Initialise le convertisseur de texte.

        Args:
            font: Police à utiliser (voir list_fonts())
            width: Largeur maximale (None = pas de limite)
        """
        self.font = font
        self.width = width

    def convert(
        self,
        text: str,
        font: Optional[str] = None,
        justify: str = "auto",
        color: Optional[str] = None,
    ) -> str:
        """
        Convertit du texte en ASCII art.

        Args:
            text: Texte à convertir
            font: Police à utiliser (override de self.font)
            justify: Justification ("auto", "left", "center", "right")
            color: Couleur ANSI (nom ou code)

        Returns:
            ASCII art du texte
        """
        font_to_use = font or self.font

        try:
            # Utilisation de pyfiglet pour la conversion
            fig = pyfiglet.Figlet(
                font=font_to_use, width=self.width or 80, justify=justify
            )
            ascii_art = fig.renderText(text)

            # Ajout de couleur si spécifié
            if color:
                ascii_art = self._add_color(ascii_art, color)

            return ascii_art
        except pyfiglet.FontNotFound:
            # Fallback sur art si la police n'existe pas dans pyfiglet
            try:
                return text2art(text, font=font_to_use)
            except:
                # Dernier fallback
                return text2art(text, font="standard")

    def convert_multiline(
        self, lines: List[str], font: Optional[str] = None, spacing: int = 1
    ) -> str:
        """
        Convertit plusieurs lignes de texte en ASCII art.

        Args:
            lines: Liste de lignes de texte
            font: Police à utiliser
            spacing: Espacement entre les lignes

        Returns:
            ASCII art multiligne
        """
        ascii_lines = []
        for line in lines:
            ascii_art = self.convert(line, font=font)
            ascii_lines.append(ascii_art)

        # Ajout d'espacement
        separator = "\n" * spacing
        return separator.join(ascii_lines)

    def create_banner(
        self,
        text: str,
        border: bool = True,
        border_char: str = "=",
        padding: int = 2,
    ) -> str:
        """
        Crée une bannière ASCII art avec bordures.

        Args:
            text: Texte de la bannière
            border: Ajouter une bordure
            border_char: Caractère de bordure
            padding: Padding horizontal

        Returns:
            Bannière ASCII
        """
        ascii_art = self.convert(text)
        lines = ascii_art.split("\n")

        if not border:
            return ascii_art

        # Calcul de la largeur maximale
        max_width = max(len(line) for line in lines if line.strip())

        # Création de la bordure
        border_line = border_char * (max_width + padding * 2)

        # Ajout de padding et bordures
        padded_lines = [border_line]
        for _ in range(padding // 2):
            padded_lines.append(border_char + " " * (max_width + (padding - 2) * 2) + border_char)

        for line in lines:
            if line.strip():
                padded_line = border_char + " " * (padding - 1) + line.ljust(max_width) + " " * (padding - 1) + border_char
                padded_lines.append(padded_line)

        for _ in range(padding // 2):
            padded_lines.append(border_char + " " * (max_width + (padding - 2) * 2) + border_char)
        padded_lines.append(border_line)

        return "\n".join(padded_lines)

    def create_gradient(self, text: str, start_color: tuple, end_color: tuple) -> str:
        """
        Crée un ASCII art avec gradient de couleurs.

        Args:
            text: Texte à convertir
            start_color: Couleur de début (r, g, b)
            end_color: Couleur de fin (r, g, b)

        Returns:
            ASCII art avec gradient
        """
        ascii_art = self.convert(text)
        lines = ascii_art.split("\n")

        # Calcul du gradient
        num_lines = len([l for l in lines if l.strip()])
        gradient_lines = []

        line_index = 0
        for line in lines:
            if not line.strip():
                gradient_lines.append(line)
                continue

            # Interpolation de couleur
            t = line_index / max(num_lines - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)

            # Application de la couleur
            colored_line = f"\033[38;2;{r};{g};{b}m{line}\033[0m"
            gradient_lines.append(colored_line)
            line_index += 1

        return "\n".join(gradient_lines)

    def create_shadow(self, text: str, shadow_offset: tuple = (2, 1)) -> str:
        """
        Crée un ASCII art avec effet d'ombre.

        Args:
            text: Texte à convertir
            shadow_offset: Décalage de l'ombre (x, y)

        Returns:
            ASCII art avec ombre
        """
        ascii_art = self.convert(text)
        lines = ascii_art.split("\n")

        offset_x, offset_y = shadow_offset

        # Création de l'ombre (caractères grisés)
        shadow_lines = []
        for _ in range(offset_y):
            shadow_lines.append("")

        for line in lines:
            shadow = " " * offset_x + self._grayscale_text(line)
            shadow_lines.append(shadow)

        # Superposition du texte original
        result_lines = []
        for i, line in enumerate(lines):
            if i < len(shadow_lines):
                # Combine shadow et texte
                shadow = shadow_lines[i]
                combined = self._overlay_strings(shadow, line)
                result_lines.append(combined)
            else:
                result_lines.append(line)

        # Ajouter les lignes d'ombre restantes
        for i in range(len(lines), len(shadow_lines)):
            result_lines.append(shadow_lines[i])

        return "\n".join(result_lines)

    def _add_color(self, text: str, color: str) -> str:
        """Ajoute une couleur ANSI au texte."""
        colors = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "bright_black": "\033[90m",
            "bright_red": "\033[91m",
            "bright_green": "\033[92m",
            "bright_yellow": "\033[93m",
            "bright_blue": "\033[94m",
            "bright_magenta": "\033[95m",
            "bright_cyan": "\033[96m",
            "bright_white": "\033[97m",
        }

        color_code = colors.get(color.lower(), "\033[0m")
        reset = "\033[0m"

        return f"{color_code}{text}{reset}"

    def _grayscale_text(self, text: str) -> str:
        """Convertit le texte en gris (pour l'ombre)."""
        return f"\033[90m{text}\033[0m"

    def _overlay_strings(self, background: str, foreground: str) -> str:
        """Superpose deux chaînes en préservant les caractères non-espaces."""
        result = list(background)
        for i, char in enumerate(foreground):
            if i < len(result) and char != " ":
                result[i] = char
            elif i >= len(result) and char != " ":
                result.append(char)

        return "".join(result)

    @staticmethod
    def list_fonts() -> List[str]:
        """Liste toutes les polices disponibles."""
        figlet_fonts = pyfiglet.FigletFont.getFonts()
        return sorted(figlet_fonts)

    @staticmethod
    def preview_fonts(text: str = "Sample", max_fonts: int = 10) -> str:
        """
        Génère un aperçu de plusieurs polices.

        Args:
            text: Texte à afficher
            max_fonts: Nombre maximum de polices à afficher

        Returns:
            Aperçu des polices
        """
        fonts = TextToASCII.list_fonts()[:max_fonts]
        previews = []

        for font in fonts:
            try:
                converter = TextToASCII(font=font)
                ascii_art = converter.convert(text)
                previews.append(f"=== {font} ===\n{ascii_art}")
            except:
                continue

        return "\n\n".join(previews)

    def create_art_decoration(self, art_name: str) -> str:
        """
        Crée une décoration ASCII à partir d'art prédéfini.

        Args:
            art_name: Nom de l'art (ex: "coffee", "heart", "random")

        Returns:
            Décoration ASCII
        """
        try:
            return art(art_name)
        except:
            return art("random")
