"""
Validateurs pour les inputs de l'API.
"""

from PIL import Image
from io import BytesIO
import base64


def validate_base64_image(base64_string):
    """
    Valide et décode une image base64.

    Args:
        base64_string: Image encodée en base64

    Returns:
        PIL.Image: Image décodée

    Raises:
        ValueError: Si l'image est invalide
    """
    try:
        # Supprimer le préfixe data:image si présent
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]

        # Décoder
        image_data = base64.b64decode(base64_string)

        # Ouvrir avec PIL
        image = Image.open(BytesIO(image_data))

        # Vérifier la taille (limite à 10 MB)
        if len(image_data) > 10 * 1024 * 1024:
            raise ValueError("Image trop grande (max 10 MB)")

        return image

    except Exception as e:
        raise ValueError(f"Image base64 invalide: {str(e)}")


def validate_width(width):
    """
    Valide la largeur de sortie.

    Args:
        width: Largeur demandée

    Returns:
        int: Largeur validée

    Raises:
        ValueError: Si la largeur est invalide
    """
    try:
        width = int(width)
        if width < 10:
            raise ValueError("Largeur minimum: 10")
        if width > 500:
            raise ValueError("Largeur maximum: 500")
        return width
    except (TypeError, ValueError) as e:
        raise ValueError(f"Largeur invalide: {str(e)}")


def validate_palette(palette):
    """
    Valide le nom de la palette.

    Args:
        palette: Nom de la palette

    Returns:
        str: Nom de palette validé

    Raises:
        ValueError: Si la palette est invalide
    """
    from ascii_generator.palettes import CharacterPalettes

    valid_palettes = CharacterPalettes.list_palettes()

    if palette not in valid_palettes:
        raise ValueError(f"Palette invalide. Valides: {', '.join(valid_palettes[:10])}...")

    return palette


def validate_color_mode(color_mode):
    """
    Valide le mode de couleur.

    Args:
        color_mode: Mode de couleur demandé

    Returns:
        str: Mode validé

    Raises:
        ValueError: Si le mode est invalide
    """
    valid_modes = ['monochrome', 'ansi', 'rgb']

    if color_mode not in valid_modes:
        raise ValueError(f"Mode invalide. Valides: {', '.join(valid_modes)}")

    return color_mode


def validate_algorithm(algorithm):
    """
    Valide l'algorithme de conversion.

    Args:
        algorithm: Algorithme demandé

    Returns:
        str: Algorithme validé

    Raises:
        ValueError: Si l'algorithme est invalide
    """
    valid_algorithms = ['luminosity', 'average', 'lightness']

    if algorithm not in valid_algorithms:
        raise ValueError(f"Algorithme invalide. Valides: {', '.join(valid_algorithms)}")

    return algorithm
