"""
Convertisseur d'animations (GIF, vidéo) en ASCII art animé.
"""

import time
import os
import sys
from typing import List, Optional
from PIL import Image
import imageio.v3 as iio
from ascii_generator.core.image_converter import ImageToASCII


class AnimationToASCII:
    """Convertit des GIFs et vidéos en animations ASCII."""

    def __init__(
        self,
        palette: str = None,
        width: int = 80,
        color_mode: str = "monochrome",
        fps: Optional[int] = None,
    ):
        """
        Initialise le convertisseur d'animations.

        Args:
            palette: Palette de caractères
            width: Largeur en caractères
            color_mode: Mode de couleur
            fps: Images par seconde (None = FPS original)
        """
        self.image_converter = ImageToASCII(
            palette=palette, width=width, color_mode=color_mode
        )
        self.fps = fps

    def convert_gif(self, gif_path: str, max_frames: Optional[int] = None) -> List[str]:
        """
        Convertit un GIF en frames ASCII.

        Args:
            gif_path: Chemin vers le GIF
            max_frames: Nombre maximum de frames (None = toutes)

        Returns:
            Liste de frames ASCII
        """
        frames = []
        try:
            gif = Image.open(gif_path)
            frame_count = 0

            while True:
                # Conversion de la frame actuelle
                ascii_frame = self.image_converter.convert(image=gif.copy())
                frames.append(ascii_frame)
                frame_count += 1

                # Limite de frames
                if max_frames and frame_count >= max_frames:
                    break

                # Passage à la frame suivante
                try:
                    gif.seek(gif.tell() + 1)
                except EOFError:
                    break

        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du GIF: {e}")

        return frames

    def convert_video(
        self, video_path: str, max_frames: Optional[int] = None, skip_frames: int = 1
    ) -> List[str]:
        """
        Convertit une vidéo en frames ASCII.

        Args:
            video_path: Chemin vers la vidéo
            max_frames: Nombre maximum de frames
            skip_frames: Sauter N frames (pour réduire la taille)

        Returns:
            Liste de frames ASCII
        """
        frames = []

        try:
            # Lecture de la vidéo avec imageio
            video_reader = iio.imiter(video_path)

            frame_count = 0
            processed_count = 0

            for frame in video_reader:
                # Sauter des frames si nécessaire
                if frame_count % (skip_frames + 1) != 0:
                    frame_count += 1
                    continue

                # Conversion de la frame
                pil_frame = Image.fromarray(frame)
                ascii_frame = self.image_converter.convert(image=pil_frame)
                frames.append(ascii_frame)

                processed_count += 1
                frame_count += 1

                # Limite de frames
                if max_frames and processed_count >= max_frames:
                    break

        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture de la vidéo: {e}")

        return frames

    def play_animation(
        self, frames: List[str], fps: Optional[int] = None, loop: bool = False
    ):
        """
        Joue une animation ASCII dans le terminal.

        Args:
            frames: Liste de frames ASCII
            fps: Images par seconde
            loop: Boucler l'animation
        """
        fps = fps or self.fps or 10
        frame_delay = 1.0 / fps

        try:
            while True:
                for frame in frames:
                    # Efface le terminal
                    self._clear_screen()

                    # Affiche la frame
                    print(frame)

                    # Attend avant la prochaine frame
                    time.sleep(frame_delay)

                if not loop:
                    break

        except KeyboardInterrupt:
            self._clear_screen()
            print("\nAnimation arrêtée.")

    def save_animation(self, frames: List[str], output_path: str):
        """
        Sauvegarde une animation ASCII dans un fichier.

        Args:
            frames: Liste de frames ASCII
            output_path: Chemin du fichier de sortie
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Animation ASCII - {len(frames)} frames\n")
            f.write(f"# Utilisez play_from_file() pour lire\n")
            f.write("---FRAME_SEPARATOR---\n")
            f.write("\n---FRAME_SEPARATOR---\n".join(frames))

    def play_from_file(self, file_path: str, fps: Optional[int] = None, loop: bool = False):
        """
        Joue une animation à partir d'un fichier sauvegardé.

        Args:
            file_path: Chemin du fichier
            fps: Images par seconde
            loop: Boucler l'animation
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extraction des frames
        parts = content.split("---FRAME_SEPARATOR---")
        frames = [part.strip() for part in parts[1:] if part.strip()]

        self.play_animation(frames, fps=fps, loop=loop)

    def create_animated_text(
        self,
        text: str,
        effects: List[str] = ["wave", "color_cycle"],
        duration: float = 5.0,
        fps: int = 20,
    ) -> List[str]:
        """
        Crée une animation de texte ASCII avec effets.

        Args:
            text: Texte à animer
            effects: Liste d'effets à appliquer
            duration: Durée en secondes
            fps: Images par seconde

        Returns:
            Liste de frames ASCII
        """
        from ascii_generator.core.text_converter import TextToASCII

        text_converter = TextToASCII(font="banner")
        base_ascii = text_converter.convert(text)

        num_frames = int(duration * fps)
        frames = []

        for i in range(num_frames):
            frame = base_ascii

            # Application des effets
            for effect in effects:
                if effect == "wave":
                    frame = self._apply_wave_effect(frame, i, num_frames)
                elif effect == "color_cycle":
                    frame = self._apply_color_cycle(frame, i, num_frames)
                elif effect == "zoom":
                    frame = self._apply_zoom_effect(base_ascii, i, num_frames)

            frames.append(frame)

        return frames

    def _apply_wave_effect(self, text: str, frame_num: int, total_frames: int) -> str:
        """Applique un effet de vague au texte."""
        lines = text.split("\n")
        waved_lines = []

        phase = (frame_num / total_frames) * 6.28  # 2π

        for line_idx, line in enumerate(lines):
            offset = int(3 * (1 + abs(1.5 * ((line_idx + phase) % 3.14))))
            waved_line = " " * offset + line
            waved_lines.append(waved_line)

        return "\n".join(waved_lines)

    def _apply_color_cycle(self, text: str, frame_num: int, total_frames: int) -> str:
        """Applique un cycle de couleurs au texte."""
        t = frame_num / total_frames

        # Cycle RGB
        r = int(127 + 127 * ((t * 2 * 3.14) % 6.28))
        g = int(127 + 127 * ((t * 2 * 3.14 + 2.09) % 6.28))
        b = int(127 + 127 * ((t * 2 * 3.14 + 4.18) % 6.28))

        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def _apply_zoom_effect(self, text: str, frame_num: int, total_frames: int) -> str:
        """Applique un effet de zoom (simulation)."""
        # Effet de zoom simplifié par espacement
        t = frame_num / total_frames
        zoom_factor = 0.5 + 1.5 * abs(0.5 - t)  # Zoom in/out

        lines = text.split("\n")
        spacing = int(zoom_factor * 2)

        return ("\n" * spacing).join(lines)

    def export_to_html(
        self, frames: List[str], output_path: str, fps: int = 10, autoplay: bool = True
    ):
        """
        Exporte l'animation en HTML avec JavaScript.

        Args:
            frames: Liste de frames ASCII
            output_path: Chemin du fichier HTML
            fps: Images par seconde
            autoplay: Démarrer automatiquement
        """
        frame_delay = int(1000 / fps)

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Animation ASCII</title>
    <style>
        body {{
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            padding: 20px;
        }}
        #ascii-art {{
            white-space: pre;
            font-size: 12px;
            line-height: 1.2;
        }}
        .controls {{
            margin-top: 20px;
        }}
        button {{
            background: #0f0;
            color: #000;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            margin-right: 10px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div id="ascii-art"></div>
    <div class="controls">
        <button onclick="toggleAnimation()">Play/Pause</button>
        <button onclick="resetAnimation()">Reset</button>
        <span id="frame-info"></span>
    </div>

    <script>
        const frames = {str([frame.replace('\n', '\\n') for frame in frames])};
        let currentFrame = 0;
        let isPlaying = {"true" if autoplay else "false"};
        let animationInterval;

        function displayFrame() {{
            document.getElementById('ascii-art').textContent = frames[currentFrame].replace(/\\\\n/g, '\\n');
            document.getElementById('frame-info').textContent = `Frame ${{currentFrame + 1}} / ${{frames.length}}`;
            currentFrame = (currentFrame + 1) % frames.length;
        }}

        function toggleAnimation() {{
            if (isPlaying) {{
                clearInterval(animationInterval);
                isPlaying = false;
            }} else {{
                animationInterval = setInterval(displayFrame, {frame_delay});
                isPlaying = true;
            }}
        }}

        function resetAnimation() {{
            currentFrame = 0;
            displayFrame();
        }}

        // Auto-start
        if (isPlaying) {{
            animationInterval = setInterval(displayFrame, {frame_delay});
        }} else {{
            displayFrame();
        }}
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _clear_screen(self):
        """Efface l'écran du terminal."""
        os.system("cls" if os.name == "nt" else "clear")

    def get_gif_info(self, gif_path: str) -> dict:
        """
        Obtient les informations sur un GIF.

        Args:
            gif_path: Chemin vers le GIF

        Returns:
            Dictionnaire avec les infos du GIF
        """
        gif = Image.open(gif_path)
        frame_count = 0

        try:
            while True:
                frame_count += 1
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

        return {
            "path": gif_path,
            "size": gif.size,
            "frames": frame_count,
            "mode": gif.mode,
        }
