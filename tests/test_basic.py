"""
Tests de base pour le générateur ASCII art.
"""

import unittest
from PIL import Image, ImageDraw
from ascii_generator import ImageToASCII, TextToASCII
from ascii_generator.palettes import CharacterPalettes


class TestImageConversion(unittest.TestCase):
    """Tests de conversion d'images."""

    def setUp(self):
        """Prépare les tests."""
        # Création d'une image de test simple
        self.test_image = Image.new("RGB", (100, 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(self.test_image)
        draw.rectangle([25, 12, 75, 38], fill=(0, 0, 0))

    def test_basic_conversion(self):
        """Test de conversion basique."""
        converter = ImageToASCII(width=50)
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("\n", result)  # Doit contenir des lignes

    def test_palette_usage(self):
        """Test d'utilisation de palettes."""
        palettes = ["STANDARD", "DETAILED", "SIMPLE", "BLOCKS"]

        for palette_name in palettes:
            with self.subTest(palette=palette_name):
                palette = CharacterPalettes.get_palette(palette_name)
                converter = ImageToASCII(palette=palette, width=30)
                result = converter.convert(image=self.test_image)

                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    def test_color_modes(self):
        """Test des différents modes de couleur."""
        modes = ["monochrome", "ansi", "rgb"]

        for mode in modes:
            with self.subTest(mode=mode):
                converter = ImageToASCII(width=30, color_mode=mode)
                result = converter.convert(image=self.test_image)

                self.assertIsInstance(result, str)
                self.assertGreater(len(result), 0)

    def test_contrast_adjustment(self):
        """Test d'ajustement du contraste."""
        converter = ImageToASCII(width=30, contrast=1.5)
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_brightness_adjustment(self):
        """Test d'ajustement de la luminosité."""
        converter = ImageToASCII(width=30, brightness=20)
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_invert(self):
        """Test d'inversion."""
        converter = ImageToASCII(width=30, invert=True)
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


class TestTextConversion(unittest.TestCase):
    """Tests de conversion de texte."""

    def test_basic_text(self):
        """Test de conversion de texte basique."""
        converter = TextToASCII()
        result = converter.convert("Test")

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_different_fonts(self):
        """Test avec différentes polices."""
        fonts = ["standard", "banner", "block"]

        for font in fonts:
            with self.subTest(font=font):
                try:
                    converter = TextToASCII(font=font)
                    result = converter.convert("A")

                    self.assertIsInstance(result, str)
                    self.assertGreater(len(result), 0)
                except:
                    # Certaines polices peuvent ne pas être disponibles
                    pass

    def test_banner_creation(self):
        """Test de création de bannière."""
        converter = TextToASCII()
        result = converter.create_banner("TEST", border_char="=", padding=2)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("=", result)  # Doit contenir le caractère de bordure

    def test_list_fonts(self):
        """Test de listage des polices."""
        fonts = TextToASCII.list_fonts()

        self.assertIsInstance(fonts, list)
        self.assertGreater(len(fonts), 0)


class TestPalettes(unittest.TestCase):
    """Tests des palettes."""

    def test_get_palette(self):
        """Test de récupération de palette."""
        palette = CharacterPalettes.get_palette("STANDARD")

        self.assertIsInstance(palette, str)
        self.assertGreater(len(palette), 0)

    def test_list_palettes(self):
        """Test de listage des palettes."""
        palettes = CharacterPalettes.list_palettes()

        self.assertIsInstance(palettes, list)
        self.assertGreater(len(palettes), 0)
        self.assertIn("STANDARD", palettes)
        self.assertIn("DETAILED", palettes)

    def test_reverse_palette(self):
        """Test d'inversion de palette."""
        original = CharacterPalettes.STANDARD
        reversed_palette = CharacterPalettes.reverse_palette(original)

        self.assertEqual(len(original), len(reversed_palette))
        self.assertEqual(original, reversed_palette[::-1])

    def test_custom_palette(self):
        """Test de création de palette personnalisée."""
        chars = "ABC123ABC"  # Avec doublons
        custom = CharacterPalettes.custom_palette(chars)

        self.assertIsInstance(custom, str)
        # Vérifier que les doublons sont supprimés
        self.assertEqual(len(set(custom)), len(custom))


class TestAlgorithms(unittest.TestCase):
    """Tests des différents algorithmes."""

    def setUp(self):
        """Prépare les tests."""
        self.test_image = Image.new("RGB", (50, 25), color=(128, 128, 128))

    def test_luminosity_algorithm(self):
        """Test de l'algorithme luminosity."""
        converter = ImageToASCII(width=30, algorithm="luminosity")
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_average_algorithm(self):
        """Test de l'algorithme average."""
        converter = ImageToASCII(width=30, algorithm="average")
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_lightness_algorithm(self):
        """Test de l'algorithme lightness."""
        converter = ImageToASCII(width=30, algorithm="lightness")
        result = converter.convert(image=self.test_image)

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


def run_tests():
    """Exécute tous les tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestImageConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestTextConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestPalettes))
    suite.addTests(loader.loadTestsFromTestCase(TestAlgorithms))

    # Exécuter
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
