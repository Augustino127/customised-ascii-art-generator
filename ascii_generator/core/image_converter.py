"""
Convertisseur d'images en ASCII art avec multiples algorithmes.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from typing import Optional, Tuple
from ascii_generator.palettes import CharacterPalettes


class ImageToASCII:
    """Convertit des images en ASCII art avec options avancées."""

    def __init__(
        self,
        palette: str = None,
        width: int = 100,
        color_mode: str = "monochrome",
        invert: bool = False,
        contrast: float = 1.0,
        brightness: float = 0,
        algorithm: str = "luminosity",
    ):
        """
        Initialise le convertisseur d'images.

        Args:
            palette: Palette de caractères à utiliser (défaut: STANDARD)
            width: Largeur de sortie en caractères
            color_mode: Mode de couleur ("monochrome", "ansi", "rgb")
            invert: Inverser les tons sombres/clairs
            contrast: Ajustement du contraste (0.5 à 2.0)
            brightness: Ajustement de la luminosité (-100 à 100)
            algorithm: Algorithme de conversion ("luminosity", "average", "lightness")
        """
        self.palette = palette or CharacterPalettes.STANDARD
        if invert:
            self.palette = self.palette[::-1]
        self.width = width
        self.color_mode = color_mode
        self.contrast = contrast
        self.brightness = brightness
        self.algorithm = algorithm

    def convert(
        self,
        image_path: str = None,
        image: Image.Image = None,
        maintain_aspect: bool = True,
    ) -> str:
        """
        Convertit une image en ASCII art.

        Args:
            image_path: Chemin vers l'image
            image: Objet PIL Image (alternative à image_path)
            maintain_aspect: Maintenir le ratio d'aspect

        Returns:
            Chaîne ASCII art
        """
        if image is None and image_path is None:
            raise ValueError("Soit image_path soit image doit être fourni")

        if image is None:
            image = Image.open(image_path)

        # Prétraitement de l'image
        image = self._preprocess_image(image, maintain_aspect)

        # Conversion en niveaux de gris selon l'algorithme
        grayscale = self._to_grayscale(image)

        # Génération de l'ASCII art
        ascii_art = self._generate_ascii(grayscale, image)

        return ascii_art

    def _preprocess_image(
        self, image: Image.Image, maintain_aspect: bool
    ) -> Image.Image:
        """Prétraite l'image (redimensionnement, ajustements)."""
        # Calcul de la hauteur en maintenant le ratio d'aspect
        if maintain_aspect:
            aspect_ratio = image.height / image.width
            # Correction pour la forme des caractères (environ 2:1)
            height = int(self.width * aspect_ratio * 0.55)
        else:
            height = self.width // 2

        # Redimensionnement
        image = image.resize((self.width, height), Image.Resampling.LANCZOS)

        # Ajustement du contraste
        if self.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(self.contrast)

        # Ajustement de la luminosité
        if self.brightness != 0:
            enhancer = ImageEnhance.Brightness(image)
            brightness_factor = 1.0 + (self.brightness / 100.0)
            image = enhancer.enhance(brightness_factor)

        return image

    def _to_grayscale(self, image: Image.Image) -> np.ndarray:
        """Convertit l'image en niveaux de gris selon l'algorithme choisi."""
        img_array = np.array(image)

        # Si l'image est déjà en niveaux de gris
        if len(img_array.shape) == 2:
            return img_array

        # Conversion RGB vers niveaux de gris
        if self.algorithm == "luminosity":
            # Formule perceptuelle standard (ITU-R BT.601)
            gray = (
                0.299 * img_array[:, :, 0]
                + 0.587 * img_array[:, :, 1]
                + 0.114 * img_array[:, :, 2]
            )
        elif self.algorithm == "average":
            # Simple moyenne des canaux RGB
            gray = np.mean(img_array[:, :, :3], axis=2)
        elif self.algorithm == "lightness":
            # (max(R,G,B) + min(R,G,B)) / 2
            gray = (
                np.max(img_array[:, :, :3], axis=2)
                + np.min(img_array[:, :, :3], axis=2)
            ) / 2
        else:
            # Par défaut, utilise luminosity
            gray = (
                0.299 * img_array[:, :, 0]
                + 0.587 * img_array[:, :, 1]
                + 0.114 * img_array[:, :, 2]
            )

        return gray.astype(np.uint8)

    def _generate_ascii(
        self, grayscale: np.ndarray, original_image: Image.Image
    ) -> str:
        """Génère l'ASCII art à partir des niveaux de gris."""
        ascii_chars = []
        height, width = grayscale.shape

        # Conversion de l'image originale en tableau pour les couleurs
        if self.color_mode in ["ansi", "rgb"]:
            color_array = np.array(original_image)

        for y in range(height):
            row = []
            for x in range(width):
                # Niveau de gris (0-255)
                brightness = grayscale[y, x]

                # Mapping vers la palette
                char_index = int((brightness / 255) * (len(self.palette) - 1))
                char = self.palette[char_index]

                # Ajout de couleur si nécessaire
                if self.color_mode == "ansi":
                    char = self._add_ansi_color(char, color_array[y, x])
                elif self.color_mode == "rgb":
                    char = self._add_rgb_color(char, color_array[y, x])

                row.append(char)

            ascii_chars.append("".join(row))

        return "\n".join(ascii_chars)

    def _add_ansi_color(self, char: str, rgb: np.ndarray) -> str:
        """Ajoute une couleur ANSI 256 à un caractère."""
        r, g, b = rgb[:3]
        # Conversion RGB vers ANSI 256
        ansi_code = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
        return f"\033[38;5;{ansi_code}m{char}\033[0m"

    def _add_rgb_color(self, char: str, rgb: np.ndarray) -> str:
        """Ajoute une couleur RGB (truecolor) à un caractère."""
        r, g, b = rgb[:3]
        return f"\033[38;2;{r};{g};{b}m{char}\033[0m"

    def convert_with_edge_detection(
        self, image_path: str = None, image: Image.Image = None
    ) -> str:
        """
        Convertit une image en ASCII en utilisant la détection de contours.

        Args:
            image_path: Chemin vers l'image
            image: Objet PIL Image

        Returns:
            ASCII art avec contours accentués
        """
        import cv2

        if image is None:
            image = Image.open(image_path)

        # Prétraitement
        image = self._preprocess_image(image, True)

        # Conversion en OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Détection de contours avec Canny
        edges = cv2.Canny(gray, 100, 200)

        # Combinaison de l'image originale avec les contours
        combined = cv2.addWeighted(gray, 0.7, edges, 0.3, 0)

        # Génération ASCII
        return self._generate_ascii(combined, image)

    def convert_with_dithering(
        self, image_path: str = None, image: Image.Image = None, method: str = "floyd"
    ) -> str:
        """
        Convertit une image en ASCII avec dithering.

        Args:
            image_path: Chemin vers l'image
            image: Objet PIL Image
            method: Méthode de dithering ("floyd", "bayer")

        Returns:
            ASCII art avec dithering
        """
        if image is None:
            image = Image.open(image_path)

        # Prétraitement
        image = self._preprocess_image(image, True)

        if method == "floyd":
            # Floyd-Steinberg dithering
            image = image.convert("L")  # Conversion en grayscale
            dithered = self._floyd_steinberg_dithering(np.array(image))
        elif method == "bayer":
            # Bayer matrix dithering
            dithered = self._bayer_dithering(np.array(image.convert("L")))
        else:
            raise ValueError(f"Méthode de dithering inconnue: {method}")

        return self._generate_ascii(dithered, image)

    def _floyd_steinberg_dithering(self, image: np.ndarray) -> np.ndarray:
        """Applique le dithering Floyd-Steinberg."""
        img = image.astype(float)
        h, w = img.shape

        for y in range(h - 1):
            for x in range(1, w - 1):
                old_pixel = img[y, x]
                new_pixel = np.round(old_pixel / 255 * (len(self.palette) - 1)) * (
                    255 / (len(self.palette) - 1)
                )
                img[y, x] = new_pixel
                quant_error = old_pixel - new_pixel

                img[y, x + 1] += quant_error * 7 / 16
                img[y + 1, x - 1] += quant_error * 3 / 16
                img[y + 1, x] += quant_error * 5 / 16
                img[y + 1, x + 1] += quant_error * 1 / 16

        return np.clip(img, 0, 255).astype(np.uint8)

    def _bayer_dithering(self, image: np.ndarray) -> np.ndarray:
        """Applique le dithering avec matrice de Bayer."""
        bayer_matrix = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16

        h, w = image.shape
        dithered = np.zeros_like(image)

        for y in range(h):
            for x in range(w):
                threshold = bayer_matrix[y % 4, x % 4] * 255
                dithered[y, x] = 255 if image[y, x] > threshold else 0

        return dithered

    def get_color_pixels(self, image: Image.Image) -> list:
        """
        Extrait les pixels colorés pour l'export HTML/SVG.

        Returns:
            Liste de tuples (x, y, char, r, g, b)
        """
        image = self._preprocess_image(image, True)
        grayscale = self._to_grayscale(image)
        color_array = np.array(image)

        pixels = []
        height, width = grayscale.shape

        for y in range(height):
            for x in range(width):
                brightness = grayscale[y, x]
                char_index = int((brightness / 255) * (len(self.palette) - 1))
                char = self.palette[char_index]
                r, g, b = color_array[y, x][:3]
                pixels.append((x, y, char, r, g, b))

        return pixels
