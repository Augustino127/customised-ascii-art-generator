"""
Palettes de caractères prédéfinies pour différents styles ASCII.
"""

class CharacterPalettes:
    """Collection de palettes de caractères pour différents effets."""

    # Palettes standard (du plus sombre au plus clair)
    STANDARD = "@%#*+=-:. "
    DETAILED = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    SIMPLE = "@#+. "
    BLOCKS = "█▓▒░ "

    # Palettes thématiques
    MATRIX = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ01 "
    BINARY = "10 "
    BRAILLE = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"

    # Palettes artistiques
    STIPPLE = "●◉○◌◦•∙⋅· "
    HEARTS = "♥♡❤💕💗💖💝💘💞 "
    STARS = "★☆✦✧✨⭐🌟 "
    MUSIC = "♫♪♬♩𝄞🎵🎶 "

    # Palettes géométriques
    CIRCLES = "●◐◑◒◓◔◕◖◗○ "
    SQUARES = "■▪▫◾◽▪️◻️ "
    TRIANGLES = "▲△▴▵▸▹►▻ "

    # Palettes pour effets spéciaux
    GRADIENT_BLOCKS = "█▓▒░ "
    SHADES = "░▒▓█ "
    LINES = "─│┌┐└┘├┤┬┴┼ "

    # Palettes d'emojis
    EMOJI_FACES = "😀😃😄😁😆😅🤣😂🙂🙃😉😊😇🥰 "
    EMOJI_NATURE = "🌲🌳🌴🌱🌿🍀🍁🍂🍃🌾 "

    @classmethod
    def get_palette(cls, name: str) -> str:
        """Récupère une palette par son nom."""
        return getattr(cls, name.upper(), cls.STANDARD)

    @classmethod
    def list_palettes(cls) -> list:
        """Liste toutes les palettes disponibles."""
        return [
            attr for attr in dir(cls)
            if not attr.startswith('_') and attr.isupper()
        ]

    @classmethod
    def reverse_palette(cls, palette: str) -> str:
        """Inverse l'ordre d'une palette."""
        return palette[::-1]

    @classmethod
    def custom_palette(cls, chars: str) -> str:
        """Crée une palette personnalisée à partir d'une chaîne."""
        # Supprime les doublons tout en préservant l'ordre
        seen = set()
        result = []
        for char in chars:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)


class ColorSchemes:
    """Schémas de couleurs ANSI pour ASCII art coloré."""

    MONOCHROME = None
    GRAYSCALE = "grayscale"
    RGB = "rgb"
    ANSI_16 = "ansi16"
    ANSI_256 = "ansi256"

    # Thèmes de couleurs prédéfinis
    CYBERPUNK = {
        'primary': (0, 255, 255),    # Cyan
        'secondary': (255, 0, 255),  # Magenta
        'accent': (255, 255, 0),     # Yellow
    }

    MATRIX = {
        'primary': (0, 255, 0),      # Green
        'secondary': (0, 200, 0),    # Dark green
        'accent': (0, 100, 0),       # Darker green
    }

    RETRO = {
        'primary': (255, 165, 0),    # Orange
        'secondary': (255, 105, 180), # Pink
        'accent': (138, 43, 226),    # Purple
    }

    FIRE = {
        'primary': (255, 0, 0),      # Red
        'secondary': (255, 165, 0),  # Orange
        'accent': (255, 255, 0),     # Yellow
    }

    OCEAN = {
        'primary': (0, 119, 190),    # Blue
        'secondary': (0, 180, 216),  # Cyan
        'accent': (144, 224, 239),   # Light cyan
    }


class ArtisticStyles:
    """Styles artistiques prédéfinis combinant palettes et effets."""

    VINTAGE = {
        'palette': CharacterPalettes.DETAILED,
        'color_scheme': ColorSchemes.MONOCHROME,
        'contrast': 1.2,
        'brightness': -10,
    }

    MODERN = {
        'palette': CharacterPalettes.BLOCKS,
        'color_scheme': ColorSchemes.RGB,
        'contrast': 1.0,
        'brightness': 0,
    }

    CYBERPUNK = {
        'palette': CharacterPalettes.MATRIX,
        'color_scheme': ColorSchemes.CYBERPUNK,
        'contrast': 1.5,
        'brightness': 10,
    }

    MINIMALIST = {
        'palette': CharacterPalettes.SIMPLE,
        'color_scheme': ColorSchemes.MONOCHROME,
        'contrast': 0.8,
        'brightness': 0,
    }

    STIPPLE = {
        'palette': CharacterPalettes.STIPPLE,
        'color_scheme': ColorSchemes.MONOCHROME,
        'contrast': 1.3,
        'brightness': 5,
    }
