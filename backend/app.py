"""
Backend Flask pour le générateur ASCII art.
API REST pour conversion d'images, texte et effets.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Ajouter le parent directory au path pour importer ascii_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

# Configuration CORS pour permettre les appels depuis GitHub Pages
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/')
def home():
    """Page d'accueil de l'API."""
    return jsonify({
        'name': 'ASCII Art Generator API',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'health': '/api/health',
            'convert_image': '/api/convert/image',
            'convert_text': '/api/convert/text',
            'palettes': '/api/palettes',
            'fonts': '/api/fonts',
            'effects': '/api/effects'
        },
        'docs': 'https://github.com/Augustino127/customised-ascii-art-generator'
    })


@app.route('/api/health')
def health():
    """Endpoint de santé pour vérifier que l'API fonctionne."""
    return jsonify({
        'status': 'healthy',
        'message': 'ASCII Art Generator API is running'
    })


@app.errorhandler(404)
def not_found(error):
    """Gestion des erreurs 404."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Gestion des erreurs 500."""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An error occurred while processing your request'
    }), 500


if __name__ == '__main__':
    # Port pour Render (ou 5000 en local)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
