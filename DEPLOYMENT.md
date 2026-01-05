# 🚀 Guide de Déploiement

Ce guide explique comment déployer l'application web complète avec backend sur Render et frontend sur GitHub Pages.

## Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (GitHub Pages)                │
│  - Interface web statique               │
│  - HTML/CSS/JavaScript                  │
│  - URL: augustino127.github.io/...     │
└──────────────┬──────────────────────────┘
               │ API Calls (HTTPS)
               ↓
┌─────────────────────────────────────────┐
│  Backend (Render)                       │
│  - API Flask Python                     │
│  - Routes de conversion                 │
│  - URL: ascii-art-api.onrender.com     │
└─────────────────────────────────────────┘
```

## Partie 1 : Déployer le Backend sur Render

### Étape 1 : Créer un compte Render

1. Allez sur [render.com](https://render.com)
2. Créez un compte (gratuit)
3. Connectez votre compte GitHub

### Étape 2 : Créer le Web Service

1. Cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre repository GitHub:
   - `Augustino127/customised-ascii-art-generator`
3. Configurez le service:
   - **Name**: `ascii-art-api` (ou votre choix)
   - **Region**: Oregon (Free)
   - **Branch**: `claude/ascii-art-generator-adrl8`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Variables d'environnement** (optionnelles):
   - Render définit automatiquement `PORT`

5. Cliquez sur **"Create Web Service"**

### Étape 3 : Attendre le déploiement

- Le déploiement prend 5-10 minutes
- Render détectera automatiquement `render.yaml`
- Une fois terminé, vous obtiendrez une URL:
  ```
  https://ascii-art-api.onrender.com
  ```

### Étape 4 : Tester l'API

Testez que l'API fonctionne:
```bash
curl https://ascii-art-api.onrender.com/api/health
```

Réponse attendue:
```json
{
  "status": "healthy",
  "message": "ASCII Art Generator API is running"
}
```

## Partie 2 : Déployer le Frontend sur GitHub Pages

### Étape 1 : Mettre à jour la configuration API

1. Éditez `docs/js/config.js`:
```javascript
// Remplacez l'URL de développement par l'URL Render
const API_URL = 'https://ascii-art-api.onrender.com';
```

2. Commitez le changement:
```bash
git add docs/js/config.js
git commit -m "config: Mise à jour URL API pour production"
git push origin claude/ascii-art-generator-adrl8
```

### Étape 2 : Activer GitHub Pages

1. Allez sur votre repository GitHub
2. **Settings** → **Pages**
3. Configuration:
   - **Source**: Deploy from a branch
   - **Branch**: `claude/ascii-art-generator-adrl8`
   - **Folder**: `/docs`
4. Cliquez sur **"Save"**

### Étape 3 : Attendre le déploiement

- Le déploiement prend 1-2 minutes
- Votre site sera disponible à:
  ```
  https://augustino127.github.io/customised-ascii-art-generator/
  ```

### Étape 4 : Tester le site

1. Ouvrez l'URL dans votre navigateur
2. Testez la conversion d'image:
   - Uploadez une image
   - Ajustez les options
   - Cliquez sur "Générer"
3. Testez la conversion de texte:
   - Allez sur la page "Texte → ASCII"
   - Entrez du texte
   - Générez

## ⚠️ Notes Importantes sur Render Free Tier

### Cold Starts
- Après **15 minutes d'inactivité**, le service s'endort
- Le premier appel prend ~30 secondes (redémarrage)
- Solution: Utilisez un service de ping (ex: UptimeRobot)

### Limites
- **750 heures/mois** gratuites (suffisant pour usage personnel)
- **512 MB RAM**
- **100 GB bandwidth/mois**

### Keep-Alive (optionnel)

Pour éviter le cold start, créez un cron job qui ping l'API toutes les 14 minutes:

```bash
# Avec UptimeRobot (gratuit)
# 1. Créez un compte sur uptimerobot.com
# 2. Ajoutez un monitor HTTP(S)
# 3. URL: https://ascii-art-api.onrender.com/api/health
# 4. Interval: 5 minutes
```

## 🐛 Dépannage

### Backend ne démarre pas

1. Vérifiez les logs dans Render Dashboard
2. Assurez-vous que `requirements.txt` est à jour
3. Vérifiez que `gunicorn` est dans requirements.txt

### Frontend ne communique pas avec backend

1. **Erreur CORS**:
   - Vérifiez que l'URL dans `config.js` est correcte
   - L'API doit retourner les headers CORS (déjà configuré)

2. **Erreur de réseau**:
   - Ouvrez la console du navigateur (F12)
   - Vérifiez que l'URL API est accessible
   - Test manuel: `curl https://votre-api.onrender.com/api/health`

3. **Cold Start**:
   - Si première requête échoue, attendez 30s et réessayez
   - Le service démarre

### Images ne se convertissent pas

1. Vérifiez la taille de l'image (max 10 MB)
2. Format supporté: JPG, PNG, GIF, WebP
3. Consultez les logs Render pour erreurs backend

## 📊 Monitoring

### Logs Backend (Render)
```
1. Render Dashboard → Votre service
2. Onglet "Logs"
3. Voir les requêtes en temps réel
```

### Logs Frontend (Browser)
```
1. F12 (Developer Tools)
2. Onglet "Console"
3. Voir les erreurs JavaScript
4. Onglet "Network" pour requêtes API
```

## 🔄 Mises à jour

### Mettre à jour le Backend
```bash
# Modifier le code dans backend/
git add backend/
git commit -m "fix: Correction bug conversion"
git push origin claude/ascii-art-generator-adrl8

# Render redéploiera automatiquement
```

### Mettre à jour le Frontend
```bash
# Modifier le code dans docs/
git add docs/
git commit -m "feat: Nouvelle fonctionnalité"
git push origin claude/ascii-art-generator-adrl8

# GitHub Pages redéploiera en 1-2 minutes
```

## 🎉 Félicitations !

Votre application est maintenant en ligne et accessible publiquement:

- **Frontend**: https://augustino127.github.io/customised-ascii-art-generator/
- **Backend API**: https://ascii-art-api.onrender.com

## 📝 Checklist de Déploiement

- [ ] Backend déployé sur Render
- [ ] API accessible et répond à `/api/health`
- [ ] URL API mise à jour dans `config.js`
- [ ] Frontend déployé sur GitHub Pages
- [ ] Site accessible publiquement
- [ ] Test conversion d'image fonctionne
- [ ] Test conversion de texte fonctionne
- [ ] Navigation entre pages fonctionne
- [ ] (Optionnel) Keep-alive configuré

## 🔗 Ressources

- [Documentation Render](https://render.com/docs)
- [Documentation GitHub Pages](https://docs.github.com/pages)
- [Repository du projet](https://github.com/Augustino127/customised-ascii-art-generator)
