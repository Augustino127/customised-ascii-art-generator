"""
Routes API pour informations (palettes, polices, etc.).
"""

from flask import Blueprint, jsonify
import sys
import os

# Ajouter le parent directory au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from ascii_generator.palettes import CharacterPalettes

info_bp = Blueprint('info', __name__)


@info_bp.route('/palettes', methods=['GET'])
def list_palettes():
    """
    Liste toutes les palettes disponibles avec aperçus.

    Returns:
        JSON avec liste des palettes et leurs caractères
    """
    try:
        palette_names = CharacterPalettes.list_palettes()
        palettes = []

        for name in palette_names:
            chars = CharacterPalettes.get_palette(name)
            palettes.append({
                'name': name,
                'characters': chars,
                'length': len(chars),
                'preview': chars[:30] + '...' if len(chars) > 30 else chars
            })

        return jsonify({
            'success': True,
            'palettes': palettes,
            'total': len(palettes)
        })

    except Exception as e:
        return jsonify({
            'error': 'Error listing palettes',
            'message': str(e)
        }), 500


@info_bp.route('/algorithms', methods=['GET'])
def list_algorithms():
    """
    Liste les algorithmes de conversion disponibles.

    Returns:
        JSON avec liste des algorithmes et descriptions
    """
    algorithms = [
        {
            'name': 'luminosity',
            'description': 'Formule perceptuelle standard (ITU-R BT.601)',
            'formula': '0.299*R + 0.587*G + 0.114*B',
            'recommended': True
        },
        {
            'name': 'average',
            'description': 'Simple moyenne des canaux RGB',
            'formula': '(R + G + B) / 3',
            'recommended': False
        },
        {
            'name': 'lightness',
            'description': 'Moyenne des valeurs min et max',
            'formula': '(max(R,G,B) + min(R,G,B)) / 2',
            'recommended': False
        }
    ]

    return jsonify({
        'success': True,
        'algorithms': algorithms
    })


@info_bp.route('/color-modes', methods=['GET'])
def list_color_modes():
    """
    Liste les modes de couleur disponibles.

    Returns:
        JSON avec liste des modes de couleur
    """
    color_modes = [
        {
            'name': 'monochrome',
            'description': 'Noir et blanc, pas de couleurs',
            'recommended': True
        },
        {
            'name': 'ansi',
            'description': 'Couleurs ANSI 256 (compatibilité terminaux)',
            'colors': 256
        },
        {
            'name': 'rgb',
            'description': 'Couleurs RGB truecolor (16.7 millions de couleurs)',
            'colors': 16777216,
            'recommended': True
        }
    ]

    return jsonify({
        'success': True,
        'color_modes': color_modes
    })


@info_bp.route('/effects', methods=['GET'])
def list_effects():
    """
    Liste les effets disponibles.

    Returns:
        JSON avec liste des effets
    """
    effects = [
        {
            'name': 'edge_detect',
            'description': 'Détection de contours avec Canny',
            'type': 'image',
            'recommended': True
        },
        {
            'name': 'dithering_floyd',
            'description': 'Dithering Floyd-Steinberg',
            'type': 'image'
        },
        {
            'name': 'dithering_bayer',
            'description': 'Dithering avec matrice de Bayer',
            'type': 'image'
        },
        {
            'name': 'gradient',
            'description': 'Gradient de couleurs',
            'type': 'text'
        },
        {
            'name': 'shadow',
            'description': 'Effet d\'ombre',
            'type': 'text'
        },
        {
            'name': 'banner',
            'description': 'Bannière avec bordures',
            'type': 'text'
        }
    ]

    return jsonify({
        'success': True,
        'effects': effects
    })
