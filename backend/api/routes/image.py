"""
Route API pour la conversion d'images.
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Ajouter le parent directory au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from ascii_generator import ImageToASCII
from ascii_generator.palettes import CharacterPalettes
from backend.api.utils.validators import (
    validate_base64_image,
    validate_width,
    validate_palette,
    validate_color_mode,
    validate_algorithm
)

image_bp = Blueprint('image', __name__)


@image_bp.route('/convert/image', methods=['POST'])
def convert_image():
    """
    Convertit une image en ASCII art.

    Body JSON:
    {
        "image": "base64_encoded_image",
        "width": 100,
        "palette": "STANDARD",
        "color_mode": "monochrome",
        "algorithm": "luminosity",
        "contrast": 1.0,
        "brightness": 0,
        "invert": false,
        "edge_detect": false,
        "dithering": null  // "floyd" ou "bayer" ou null
    }

    Returns:
        JSON avec ascii_art, dimensions, et métadonnées
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400

        # Validation des inputs
        if 'image' not in data:
            return jsonify({
                'error': 'Missing required field: image'
            }), 400

        # Décoder et valider l'image
        image = validate_base64_image(data['image'])

        # Paramètres avec valeurs par défaut
        width = validate_width(data.get('width', 100))
        palette_name = validate_palette(data.get('palette', 'STANDARD'))
        color_mode = validate_color_mode(data.get('color_mode', 'monochrome'))
        algorithm = validate_algorithm(data.get('algorithm', 'luminosity'))

        contrast = float(data.get('contrast', 1.0))
        brightness = int(data.get('brightness', 0))
        invert = bool(data.get('invert', False))
        edge_detect = bool(data.get('edge_detect', False))
        dithering = data.get('dithering')

        # Limites de sécurité
        contrast = max(0.5, min(2.0, contrast))
        brightness = max(-100, min(100, brightness))

        # Récupération de la palette
        palette = CharacterPalettes.get_palette(palette_name)

        # Création du convertisseur
        converter = ImageToASCII(
            palette=palette,
            width=width,
            color_mode=color_mode,
            invert=invert,
            contrast=contrast,
            brightness=brightness,
            algorithm=algorithm
        )

        # Conversion avec options
        if edge_detect:
            ascii_art = converter.convert_with_edge_detection(image=image)
        elif dithering in ['floyd', 'bayer']:
            ascii_art = converter.convert_with_dithering(image=image, method=dithering)
        else:
            ascii_art = converter.convert(image=image)

        # Calcul des dimensions
        lines = ascii_art.split('\n')
        height = len(lines)
        actual_width = max(len(line) for line in lines) if lines else 0

        return jsonify({
            'success': True,
            'ascii_art': ascii_art,
            'metadata': {
                'width': actual_width,
                'height': height,
                'palette': palette_name,
                'color_mode': color_mode,
                'algorithm': algorithm,
                'edge_detect': edge_detect,
                'dithering': dithering,
                'original_size': image.size
            }
        })

    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400

    except Exception as e:
        return jsonify({
            'error': 'Processing error',
            'message': str(e)
        }), 500
