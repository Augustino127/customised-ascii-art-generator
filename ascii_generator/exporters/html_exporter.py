"""
Exporteur HTML pour ASCII art.
"""

from typing import Optional


class HTMLExporter:
    """Exporte l'ASCII art en HTML avec styles."""

    def __init__(
        self,
        background_color: str = "#000000",
        text_color: str = "#00ff00",
        font_family: str = "'Courier New', monospace",
        font_size: int = 12,
    ):
        """
        Initialise l'exporteur HTML.

        Args:
            background_color: Couleur de fond
            text_color: Couleur du texte
            font_family: Police de caractères
            font_size: Taille de la police
        """
        self.background_color = background_color
        self.text_color = text_color
        self.font_family = font_family
        self.font_size = font_size

    def export(
        self,
        ascii_art: str,
        output_path: str,
        title: str = "ASCII Art",
        include_download: bool = True,
    ):
        """
        Exporte l'ASCII art en fichier HTML.

        Args:
            ascii_art: Chaîne ASCII art
            output_path: Chemin du fichier de sortie
            title: Titre de la page
            include_download: Inclure bouton de téléchargement
        """
        # Échappement HTML
        escaped_art = ascii_art.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        download_button = ""
        if include_download:
            download_button = """
            <button onclick="downloadAsText()" class="download-btn">
                💾 Télécharger en TXT
            </button>
            <script>
                function downloadAsText() {
                    const text = document.getElementById('ascii-art').textContent;
                    const blob = new Blob([text], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'ascii-art.txt';
                    a.click();
                    URL.revokeObjectURL(url);
                }
            </script>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: {self.background_color};
            color: {self.text_color};
            font-family: {self.font_family};
            padding: 20px;
            overflow-x: auto;
        }}

        .container {{
            max-width: 100%;
            margin: 0 auto;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 20px;
            font-size: 24px;
            text-shadow: 0 0 10px {self.text_color};
        }}

        #ascii-art {{
            white-space: pre;
            font-size: {self.font_size}px;
            line-height: 1.2;
            display: inline-block;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border: 2px solid {self.text_color};
            border-radius: 5px;
            box-shadow: 0 0 20px {self.text_color}33;
        }}

        .controls {{
            margin-top: 20px;
            text-align: center;
        }}

        .download-btn {{
            background-color: {self.text_color};
            color: {self.background_color};
            border: none;
            padding: 12px 24px;
            font-family: {self.font_family};
            font-size: 14px;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s;
        }}

        .download-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 15px {self.text_color};
        }}

        @media print {{
            body {{
                background-color: white;
                color: black;
            }}
            .controls {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div id="ascii-art">{escaped_art}</div>
        <div class="controls">
            {download_button}
        </div>
    </div>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def export_with_rgb(
        self,
        pixels: list,
        width: int,
        height: int,
        output_path: str,
        title: str = "ASCII Art (Color)",
    ):
        """
        Exporte l'ASCII art coloré (RGB) en HTML.

        Args:
            pixels: Liste de tuples (x, y, char, r, g, b)
            width: Largeur en caractères
            height: Hauteur en caractères
            output_path: Chemin du fichier de sortie
            title: Titre de la page
        """
        # Création d'une grille HTML avec couleurs
        rows = [["" for _ in range(width)] for _ in range(height)]

        for x, y, char, r, g, b in pixels:
            if 0 <= y < height and 0 <= x < width:
                color = f"rgb({r},{g},{b})"
                rows[y][x] = f'<span style="color:{color}">{char}</span>'

        # Assemblage des lignes
        html_rows = []
        for row in rows:
            html_rows.append("".join(row))

        ascii_html = "<br>".join(html_rows)

        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            background-color: {self.background_color};
            font-family: {self.font_family};
            padding: 20px;
            overflow-x: auto;
        }}

        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }}

        #ascii-art {{
            font-size: {self.font_size}px;
            line-height: 1.2;
            letter-spacing: 0;
            display: inline-block;
        }}

        .container {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div id="ascii-art">{ascii_html}</div>
    </div>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def export_interactive(
        self,
        ascii_art: str,
        output_path: str,
        title: str = "ASCII Art Interactive",
    ):
        """
        Exporte avec contrôles interactifs (zoom, couleurs, etc.).

        Args:
            ascii_art: Chaîne ASCII art
            output_path: Chemin du fichier de sortie
            title: Titre de la page
        """
        escaped_art = ascii_art.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .controls {{
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: #111;
            border-radius: 5px;
        }}

        .control-group {{
            display: inline-block;
            margin: 10px;
        }}

        label {{
            display: block;
            margin-bottom: 5px;
        }}

        input[type="range"] {{
            width: 150px;
        }}

        input[type="color"] {{
            width: 50px;
            height: 30px;
            border: none;
            cursor: pointer;
        }}

        button {{
            background: #0f0;
            color: #000;
            border: none;
            padding: 8px 16px;
            cursor: pointer;
            margin: 5px;
            border-radius: 3px;
        }}

        #ascii-art {{
            white-space: pre;
            font-size: 12px;
            line-height: 1.2;
            transition: all 0.3s;
            display: inline-block;
        }}

        .container {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="controls">
        <div class="control-group">
            <label>Taille: <span id="size-value">12</span>px</label>
            <input type="range" id="font-size" min="6" max="24" value="12">
        </div>

        <div class="control-group">
            <label>Couleur du texte</label>
            <input type="color" id="text-color" value="#00ff00">
        </div>

        <div class="control-group">
            <label>Couleur de fond</label>
            <input type="color" id="bg-color" value="#000000">
        </div>

        <div class="control-group">
            <button onclick="invertColors()">Inverser couleurs</button>
            <button onclick="resetStyles()">Réinitialiser</button>
            <button onclick="downloadAsText()">💾 Télécharger</button>
        </div>
    </div>

    <div class="container">
        <div id="ascii-art">{escaped_art}</div>
    </div>

    <script>
        const asciiArt = document.getElementById('ascii-art');
        const fontSizeSlider = document.getElementById('font-size');
        const sizeValue = document.getElementById('size-value');
        const textColorPicker = document.getElementById('text-color');
        const bgColorPicker = document.getElementById('bg-color');

        fontSizeSlider.addEventListener('input', (e) => {{
            const size = e.target.value;
            asciiArt.style.fontSize = size + 'px';
            sizeValue.textContent = size;
        }});

        textColorPicker.addEventListener('input', (e) => {{
            asciiArt.style.color = e.target.value;
        }});

        bgColorPicker.addEventListener('input', (e) => {{
            document.body.style.backgroundColor = e.target.value;
        }});

        function invertColors() {{
            const currentText = asciiArt.style.color || '#00ff00';
            const currentBg = document.body.style.backgroundColor || '#000000';
            asciiArt.style.color = currentBg;
            document.body.style.backgroundColor = currentText;
            textColorPicker.value = currentBg;
            bgColorPicker.value = currentText;
        }}

        function resetStyles() {{
            asciiArt.style.fontSize = '12px';
            asciiArt.style.color = '#00ff00';
            document.body.style.backgroundColor = '#000000';
            fontSizeSlider.value = 12;
            sizeValue.textContent = '12';
            textColorPicker.value = '#00ff00';
            bgColorPicker.value = '#000000';
        }}

        function downloadAsText() {{
            const text = asciiArt.textContent;
            const blob = new Blob([text], {{ type: 'text/plain' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ascii-art.txt';
            a.click();
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
