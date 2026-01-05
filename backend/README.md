# Backend API - ASCII Art Generator

API REST Flask pour le générateur ASCII art.

## Installation locale

```bash
cd backend
pip install -r requirements.txt
```

## Lancement local

```bash
python app.py
```

L'API sera accessible sur `http://localhost:5000`

## Endpoints

### Santé
- `GET /` - Informations sur l'API
- `GET /api/health` - Vérification de santé

### Conversion (à venir)
- `POST /api/convert/image` - Conversion d'images
- `POST /api/convert/text` - Conversion de texte

### Informations (à venir)
- `GET /api/palettes` - Liste des palettes
- `GET /api/fonts` - Liste des polices

## Déploiement sur Render

1. Pusher le code sur GitHub
2. Connecter le repo à Render
3. Render détectera automatiquement `render.yaml`
4. L'API sera déployée automatiquement

## Variables d'environnement

- `PORT` - Port d'écoute (défini par Render)
- `PYTHON_VERSION` - Version Python (3.11.0)
