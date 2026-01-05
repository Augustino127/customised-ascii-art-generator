# 🎨 Générateur ASCII Art Personnalisé

Un générateur ASCII art **ultra-complet** avec fonctionnalités avancées et innovations uniques.

## 🌐 Application Web

**✨ Utilisez le générateur en ligne :** [augustino127.github.io/customised-ascii-art-generator](https://augustino127.github.io/customised-ascii-art-generator/)

L'application web permet de :
- 📤 **Upload d'images** directement dans le navigateur
- ⚙️ **Toutes les options** de conversion en temps réel
- 🎨 **Prévisualisation instantanée**
- 💾 **Téléchargement** des résultats
- 📱 **Interface responsive** mobile-friendly

**Architecture :**
- Frontend : GitHub Pages (HTML/CSS/JavaScript)
- Backend : Render.com (Flask API Python)
- Communication : API REST avec CORS

## ✨ Fonctionnalités

### 🖼️ Conversion d'Images
- **Multiples algorithmes** de conversion (luminosité, moyenne, lightness)
- **Palettes personnalisables** (15+ palettes prédéfinies)
- **Modes de couleur** : Monochrome, ANSI 256, RGB truecolor
- **Ajustements avancés** : Contraste, luminosité, inversion
- **Détection de contours** avec Canny edge detection
- **Dithering** : Floyd-Steinberg et Bayer matrix

### 📝 Conversion de Texte
- **100+ polices ASCII** (via pyfiglet)
- **Bannières** avec bordures personnalisables
- **Gradients de couleurs**
- **Effets d'ombre**
- **Texte multiligne** avec espacement

### 🎬 Animations ASCII
- **Conversion GIF → ASCII animé**
- **Conversion vidéo → ASCII animé** (MP4, AVI, MOV, MKV)
- **Lecture en temps réel** dans le terminal
- **Export HTML animé** avec JavaScript
- **Animations de texte** avec effets (wave, color cycle, zoom)

### 🎭 Effets Artistiques
- **Stippling/Pointillisme**
- **Halftone** (trame de points)
- **Edge glow** (contours lumineux)
- **Effet vintage/sépia**
- **Effet glitch/corruption**
- **Effet cyberpunk** (cyan/magenta)
- **3D anaglyphe** (rouge/cyan)
- **Cartes de profondeur**

### 📤 Export Multi-formats
- **HTML** avec styles CSS personnalisés
- **HTML interactif** (contrôles zoom, couleurs)
- **SVG vectoriel** avec effets optionnels
- **Texte brut** (.txt)
- **Fichiers d'animation** personnalisés

## 🚀 Installation

```bash
# Installation des dépendances
pip install -r requirements.txt

# Installation du package
pip install -e .
```

## 💻 Utilisation

### CLI (Ligne de commande)

#### Conversion d'images
```bash
# Basique
ascii-gen image photo.jpg

# Avec options avancées
ascii-gen image photo.jpg --width 120 --palette DETAILED --color rgb --contrast 1.5

# Détection de contours
ascii-gen image photo.jpg --edge-detect

# Dithering Floyd-Steinberg
ascii-gen image photo.jpg --dithering floyd

# Export HTML et SVG
ascii-gen image photo.jpg --export-html output.html --export-svg output.svg
```

#### Conversion de texte
```bash
# Basique
ascii-gen text "Hello World"

# Avec police et couleur
ascii-gen text "ASCII Art" --font banner --color cyan

# Bannière avec bordures
ascii-gen text "TITLE" --banner

# Gradient de couleurs
ascii-gen text "Gradient" --gradient

# Avec ombre
ascii-gen text "Shadow" --shadow
```

#### Animations
```bash
# Convertir un GIF
ascii-gen animate animation.gif --width 80 --play

# Convertir une vidéo
ascii-gen animate video.mp4 --width 100 --max-frames 100 --skip-frames 2

# Export HTML animé
ascii-gen animate animation.gif --export-html animation.html --fps 15

# Sauvegarder et jouer en boucle
ascii-gen animate animation.gif --save output.txt --play --loop
```

#### Effets artistiques
```bash
# Stippling
ascii-gen effect photo.jpg --effect stipple --output stipple.jpg

# Halftone
ascii-gen effect photo.jpg --effect halftone --output halftone.jpg

# Effet cyberpunk
ascii-gen effect photo.jpg --effect cyberpunk --output cyber.jpg

# Effet 3D
ascii-gen effect photo.jpg --effect 3d --output 3d.jpg

# Glitch
ascii-gen effect photo.jpg --effect glitch --output glitch.jpg
```

#### Informations
```bash
# Liste des palettes
ascii-gen list-palettes

# Liste des polices
ascii-gen list-fonts

# Aperçu des polices
ascii-gen preview-fonts --text "Demo" --max-fonts 5

# Styles prédéfinis
ascii-gen styles
```

### Mode Interactif

```bash
ascii-gen interactive
```

Interface interactive avec:
- Autocomplétion des commandes
- Historique des commandes
- Prévisualisation en temps réel
- Sauvegarde facile

### API Python

#### Conversion d'images

```python
from ascii_generator import ImageToASCII
from ascii_generator.palettes import CharacterPalettes

# Création du convertisseur
converter = ImageToASCII(
    palette=CharacterPalettes.DETAILED,
    width=100,
    color_mode="ansi",
    contrast=1.2
)

# Conversion
ascii_art = converter.convert("photo.jpg")
print(ascii_art)

# Avec détection de contours
ascii_art = converter.convert_with_edge_detection("photo.jpg")

# Avec dithering
ascii_art = converter.convert_with_dithering("photo.jpg", method="floyd")
```

#### Conversion de texte

```python
from ascii_generator import TextToASCII

converter = TextToASCII(font="banner")

# Conversion simple
ascii_art = converter.convert("Hello", color="cyan")

# Bannière
banner = converter.create_banner("TITLE", border_char="=", padding=3)

# Gradient
gradient = converter.create_gradient(
    "Gradient",
    start_color=(0, 255, 255),  # Cyan
    end_color=(255, 0, 255)     # Magenta
)

# Avec ombre
shadow = converter.create_shadow("Shadow", shadow_offset=(3, 2))
```

#### Animations

```python
from ascii_generator import AnimationToASCII

converter = AnimationToASCII(width=80, fps=15)

# Conversion GIF
frames = converter.convert_gif("animation.gif", max_frames=50)

# Lecture
converter.play_animation(frames, loop=True)

# Sauvegarde
converter.save_animation(frames, "output.txt")

# Export HTML
converter.export_to_html(frames, "animation.html", fps=15)

# Animation de texte avec effets
text_frames = converter.create_animated_text(
    "HELLO",
    effects=["wave", "color_cycle"],
    duration=5.0,
    fps=20
)
```

#### Effets artistiques

```python
from ascii_generator.effects import ArtisticEffects
from PIL import Image

effects = ArtisticEffects()
image = Image.open("photo.jpg")

# Stippling
stippled = effects.apply_stippling(image, density=2000)

# Halftone
halftone = effects.apply_halftone(image, dot_size=5)

# Effet cyberpunk
cyber = effects.apply_cyberpunk_effect(image)

# Effet 3D
anaglyph = effects.apply_3d_effect(image, depth=8)

# Glitch
glitched = effects.apply_glitch_effect(image, intensity=15)
```

#### Export

```python
from ascii_generator.exporters import HTMLExporter, SVGExporter

# Export HTML
html_exporter = HTMLExporter(
    background_color="#000000",
    text_color="#00ff00",
    font_size=12
)
html_exporter.export(ascii_art, "output.html", title="Mon ASCII Art")

# Export HTML interactif
html_exporter.export_interactive(ascii_art, "interactive.html")

# Export SVG
svg_exporter = SVGExporter(font_size=12)
svg_exporter.export(ascii_art, "output.svg")

# Export SVG avec effets
svg_exporter.export_with_effects(
    ascii_art,
    "output_glow.svg",
    glow=True,
    shadow=True
)
```

## 🎨 Palettes Disponibles

- `STANDARD` - Palette standard (@%#*+=-:. )
- `DETAILED` - Palette détaillée (70+ caractères)
- `SIMPLE` - Palette simple (@#+. )
- `BLOCKS` - Blocs Unicode (█▓▒░ )
- `MATRIX` - Style Matrix (caractères japonais)
- `BINARY` - Binaire (10 )
- `BRAILLE` - Caractères Braille
- `STIPPLE` - Pointillisme (●◉○◌◦•∙⋅· )
- `HEARTS` - Cœurs (♥♡❤💕💗)
- `STARS` - Étoiles (★☆✦✧✨)
- `MUSIC` - Notes de musique (♫♪♬♩)
- `CIRCLES` - Cercles (●◐◑◒◓)
- `SQUARES` - Carrés (■▪▫◾◽)
- `EMOJI_FACES` - Visages emoji
- `EMOJI_NATURE` - Nature emoji

## 🎭 Styles Artistiques

Styles prédéfinis combinant palette + effets:
- `VINTAGE` - Rétro monochrome
- `MODERN` - Blocs avec couleurs RGB
- `CYBERPUNK` - Style Matrix avec cyan/magenta
- `MINIMALIST` - Palette simple épurée
- `STIPPLE` - Pointillisme artistique

## 📋 Exemples

### Exemple 1: Portrait en ASCII
```bash
ascii-gen image portrait.jpg \
  --width 150 \
  --palette DETAILED \
  --contrast 1.3 \
  --edge-detect \
  --export-html portrait.html
```

### Exemple 2: Logo avec animation
```bash
# Créer le logo
ascii-gen text "MY LOGO" --font banner --gradient > logo.txt

# Créer une animation
ascii-gen animate logo_animation.gif --export-html logo.html --fps 20
```

### Exemple 3: Effet cyberpunk
```bash
# Appliquer l'effet
ascii-gen effect photo.jpg --effect cyberpunk --output cyber.jpg

# Convertir en ASCII
ascii-gen image cyber.jpg --palette MATRIX --color ansi --width 120
```

## 🔧 Configuration Avancée

### Créer une palette personnalisée

```python
from ascii_generator.palettes import CharacterPalettes

# Palette personnalisée
custom = CharacterPalettes.custom_palette("@#$%&*+=- ")

converter = ImageToASCII(palette=custom)
```

### Algorithmes de conversion

- `luminosity` (défaut) - Formule perceptuelle ITU-R BT.601
- `average` - Moyenne simple des canaux RGB
- `lightness` - (max + min) / 2

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests
- Partager vos créations

## 📄 Licence

MIT License - voir LICENSE pour plus de détails

## 🙏 Remerciements

Inspiré par les meilleurs générateurs ASCII existants :
- [ASCII Art Generator](https://ascii-images.com/)
- [TAAG](https://patorjk.com/software/taag/)
- [a1.art AI ASCII Generator](https://a1.art/features/ai-ascii-art-art-generator)

---

**Créé avec ❤️ par l'équipe ASCII Art Generator**
