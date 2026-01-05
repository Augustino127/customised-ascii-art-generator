"""
Effets artistiques avancés pour ASCII art.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from typing import Tuple, Optional
import cv2


class ArtisticEffects:
    """Effets artistiques pour améliorer l'ASCII art."""

    @staticmethod
    def apply_stippling(
        image: Image.Image, density: int = 1000, size_range: Tuple[int, int] = (1, 5)
    ) -> Image.Image:
        """
        Applique un effet de stippling (pointillisme).

        Args:
            image: Image PIL
            density: Nombre de points
            size_range: Plage de tailles des points (min, max)

        Returns:
            Image avec effet de stippling
        """
        width, height = image.size
        img_array = np.array(image.convert("L"))

        # Création d'une nouvelle image blanche
        stippled = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(stippled)

        # Génération de points proportionnels à l'intensité
        for _ in range(density):
            # Sélection aléatoire d'un pixel avec probabilité basée sur l'intensité
            weights = 255 - img_array.flatten()
            weights = weights / weights.sum()

            idx = np.random.choice(len(weights), p=weights)
            y, x = divmod(idx, width)

            # Taille du point basée sur l'intensité locale
            intensity = img_array[y, x]
            size = int(size_range[0] + (1 - intensity / 255) * (size_range[1] - size_range[0]))

            # Dessine le point
            draw.ellipse([x - size, y - size, x + size, y + size], fill=0)

        return stippled

    @staticmethod
    def apply_halftone(
        image: Image.Image, dot_size: int = 5, angle: float = 22.5
    ) -> Image.Image:
        """
        Applique un effet de trame halftone.

        Args:
            image: Image PIL
            dot_size: Taille des points
            angle: Angle de la trame (degrés)

        Returns:
            Image avec effet halftone
        """
        gray = image.convert("L")
        width, height = gray.size

        # Création de l'image de sortie
        halftone = Image.new("L", (width, height), 255)
        draw = ImageDraw.Draw(halftone)

        img_array = np.array(gray)

        # Grille de points
        for y in range(0, height, dot_size):
            for x in range(0, width, dot_size):
                # Calcul de l'intensité moyenne de la zone
                region = img_array[
                    y : min(y + dot_size, height), x : min(x + dot_size, width)
                ]
                avg_intensity = region.mean()

                # Taille du point proportionnelle à l'intensité
                radius = int((1 - avg_intensity / 255) * dot_size / 2)

                if radius > 0:
                    cx, cy = x + dot_size // 2, y + dot_size // 2
                    draw.ellipse(
                        [cx - radius, cy - radius, cx + radius, cy + radius], fill=0
                    )

        return halftone

    @staticmethod
    def apply_edge_glow(
        image: Image.Image, intensity: float = 2.0, blur_radius: int = 5
    ) -> Image.Image:
        """
        Applique un effet de glow sur les contours.

        Args:
            image: Image PIL
            intensity: Intensité du glow
            blur_radius: Rayon du flou

        Returns:
            Image avec effet de glow
        """
        # Conversion en OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Détection de contours
        edges = cv2.Canny(gray, 100, 200)

        # Application du flou aux contours
        blurred_edges = cv2.GaussianBlur(edges, (blur_radius * 2 + 1, blur_radius * 2 + 1), 0)

        # Augmentation de l'intensité
        glowing_edges = np.clip(blurred_edges * intensity, 0, 255).astype(np.uint8)

        # Combinaison avec l'image originale
        result = cv2.addWeighted(gray, 0.7, glowing_edges, 0.3, 0)

        return Image.fromarray(result)

    @staticmethod
    def apply_ascii_mosaic(
        image: Image.Image, tile_size: int = 8, chars: str = "@%#*+=-:. "
    ) -> Image.Image:
        """
        Crée un effet de mosaïque avec caractères ASCII.

        Args:
            image: Image PIL
            tile_size: Taille des tuiles
            chars: Caractères à utiliser

        Returns:
            Image en mosaïque
        """
        width, height = image.size
        gray = image.convert("L")
        img_array = np.array(gray)

        # Création d'une nouvelle image
        mosaic = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(mosaic)

        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                # Calcul de l'intensité moyenne
                region = img_array[
                    y : min(y + tile_size, height), x : min(x + tile_size, width)
                ]
                avg_intensity = region.mean()

                # Sélection du caractère
                char_idx = int((avg_intensity / 255) * (len(chars) - 1))
                char = chars[char_idx]

                # Couleur de la région (si image couleur)
                if image.mode == "RGB":
                    color_region = np.array(image)[
                        y : min(y + tile_size, height), x : min(x + tile_size, width)
                    ]
                    avg_color = tuple(color_region.mean(axis=(0, 1)).astype(int))
                else:
                    intensity = int(avg_intensity)
                    avg_color = (intensity, intensity, intensity)

                # Dessine le caractère
                draw.text((x, y), char, fill=avg_color)

        return mosaic

    @staticmethod
    def apply_3d_effect(
        image: Image.Image, depth: int = 5, angle: float = 45
    ) -> Image.Image:
        """
        Applique un effet 3D (anaglyphe rouge/cyan).

        Args:
            image: Image PIL
            depth: Profondeur de l'effet 3D
            angle: Angle de décalage

        Returns:
            Image avec effet 3D
        """
        width, height = image.size
        gray = image.convert("L")

        # Calcul du décalage
        offset_x = int(depth * np.cos(np.radians(angle)))
        offset_y = int(depth * np.sin(np.radians(angle)))

        # Création des canaux rouge et cyan
        red_channel = gray.copy()
        cyan_channel = gray.copy()

        # Décalage du canal cyan
        cyan_shifted = Image.new("L", (width, height), 0)
        cyan_shifted.paste(cyan_channel, (offset_x, offset_y))

        # Création de l'image RGB anaglyphe
        anaglyph = Image.merge(
            "RGB",
            (
                red_channel,  # Canal rouge
                cyan_shifted,  # Canal vert (cyan)
                cyan_shifted,  # Canal bleu (cyan)
            ),
        )

        return anaglyph

    @staticmethod
    def apply_depth_map(
        image: Image.Image, depth_strength: float = 1.5
    ) -> Tuple[Image.Image, np.ndarray]:
        """
        Génère une carte de profondeur à partir d'une image.

        Args:
            image: Image PIL
            depth_strength: Force de la profondeur

        Returns:
            Tuple (image originale, carte de profondeur)
        """
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Détection de contours pour estimer la profondeur
        edges = cv2.Canny(gray, 100, 200)

        # Flou gaussien pour créer des zones de profondeur
        depth_map = cv2.GaussianBlur(255 - edges, (21, 21), 0)

        # Application de la force de profondeur
        depth_map = np.clip(depth_map * depth_strength, 0, 255).astype(np.uint8)

        return image, depth_map

    @staticmethod
    def apply_vintage_effect(image: Image.Image) -> Image.Image:
        """
        Applique un effet vintage/rétro.

        Args:
            image: Image PIL

        Returns:
            Image avec effet vintage
        """
        # Conversion en sépia
        sepia = image.convert("RGB")
        width, height = sepia.size
        pixels = sepia.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]

                # Formule sépia
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                # Limitation à 255
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))

        # Ajout de bruit
        noise = np.random.randint(-20, 20, (height, width, 3))
        vintage_array = np.array(sepia) + noise
        vintage_array = np.clip(vintage_array, 0, 255).astype(np.uint8)

        return Image.fromarray(vintage_array)

    @staticmethod
    def apply_glitch_effect(
        image: Image.Image, intensity: int = 10, num_glitches: int = 5
    ) -> Image.Image:
        """
        Applique un effet glitch/corruption.

        Args:
            image: Image PIL
            intensity: Intensité du glitch
            num_glitches: Nombre de zones glitchées

        Returns:
            Image avec effet glitch
        """
        width, height = image.size
        glitched = image.copy()
        pixels = np.array(glitched)

        for _ in range(num_glitches):
            # Sélection d'une zone aléatoire
            y1 = np.random.randint(0, height - intensity)
            y2 = y1 + np.random.randint(1, intensity)
            shift = np.random.randint(-intensity, intensity)

            # Décalage horizontal de la zone
            if shift > 0:
                pixels[y1:y2, shift:] = pixels[y1:y2, :-shift]
            elif shift < 0:
                pixels[y1:y2, :shift] = pixels[y1:y2, -shift:]

            # Perturbation de couleur
            channel = np.random.randint(0, 3)
            pixels[y1:y2, :, channel] = np.roll(
                pixels[y1:y2, :, channel], np.random.randint(-10, 10)
            )

        return Image.fromarray(pixels)

    @staticmethod
    def apply_cyberpunk_effect(image: Image.Image) -> Image.Image:
        """
        Applique un effet cyberpunk (cyan/magenta).

        Args:
            image: Image PIL

        Returns:
            Image avec effet cyberpunk
        """
        # Boost des couleurs cyan et magenta
        img_array = np.array(image.convert("RGB")).astype(float)

        # Augmentation du cyan (bleu + vert)
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.3, 0, 255)  # Vert
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.5, 0, 255)  # Bleu

        # Augmentation du magenta (rouge + bleu)
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.2, 0, 255)  # Rouge

        # Augmentation du contraste
        img_array = np.clip((img_array - 128) * 1.5 + 128, 0, 255)

        return Image.fromarray(img_array.astype(np.uint8))
