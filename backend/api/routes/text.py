"""
Route API pour la conversion de texte.
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Ajouter le parent directory au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from ascii_generator import TextToASCII

text_bp = Blueprint('text', __name__)


@text_bp.route('/convert/text', methods=['POST'])
def convert_text():
    """
    Convertit du texte en ASCII art.

    Body JSON:
    {
        "text": "Hello World",
        "font": "standard",
        "width": null,
        "color": null,
        "banner": false,
        "gradient": false,
        "gradient_colors": {
            "start": [0, 255, 255],
            "end": [255, 0, 255]
        },
        "shadow": false,
        "shadow_offset": [2, 1]
    }

    Returns:
        JSON avec ascii_art et métadonnées
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No JSON data provided'
            }), 400

        # Validation des inputs
        if 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400

        text = str(data['text'])

        if len(text) == 0:
            return jsonify({
                'error': 'Text cannot be empty'
            }), 400

        if len(text) > 100:
            return jsonify({
                'error': 'Text too long (max 100 characters)'
            }), 400

        # Paramètres
        font = data.get('font', 'standard')
        width = data.get('width')
        color = data.get('color')
        banner = bool(data.get('banner', False))
        gradient = bool(data.get('gradient', False))
        shadow = bool(data.get('shadow', False))

        # Création du convertisseur
        converter = TextToASCII(font=font, width=width)

        # Conversion selon les options
        if shadow:
            shadow_offset = tuple(data.get('shadow_offset', [2, 1]))
            ascii_art = converter.create_shadow(text, shadow_offset=shadow_offset)
        elif gradient:
            gradient_colors = data.get('gradient_colors', {})
            start_color = tuple(gradient_colors.get('start', [0, 255, 255]))
            end_color = tuple(gradient_colors.get('end', [255, 0, 255]))
            ascii_art = converter.create_gradient(
                text,
                start_color=start_color,
                end_color=end_color
            )
        elif banner:
            border_char = data.get('border_char', '=')
            padding = int(data.get('padding', 2))
            ascii_art = converter.create_banner(
                text,
                border=True,
                border_char=border_char,
                padding=padding
            )
        else:
            ascii_art = converter.convert(text, color=color)

        # Calcul des dimensions
        lines = ascii_art.split('\n')
        height = len(lines)
        max_width = max(len(line) for line in lines) if lines else 0

        return jsonify({
            'success': True,
            'ascii_art': ascii_art,
            'metadata': {
                'width': max_width,
                'height': height,
                'font': font,
                'has_color': bool(color or gradient),
                'is_banner': banner,
                'has_shadow': shadow
            }
        })

    except Exception as e:
        return jsonify({
            'error': 'Processing error',
            'message': str(e)
        }), 500


@text_bp.route('/fonts', methods=['GET'])
def list_fonts():
    """
    Liste toutes les polices disponibles.

    Returns:
        JSON avec liste des polices
    """
    try:
        fonts = TextToASCII.list_fonts()

        return jsonify({
            'success': True,
            'fonts': fonts[:50],  # Limite à 50 pour la performance
            'total': len(fonts)
        })

    except Exception as e:
        return jsonify({
            'error': 'Error listing fonts',
            'message': str(e)
        }), 500
