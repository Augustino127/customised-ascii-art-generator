# Exemples d'utilisation

Ce dossier contient des exemples d'utilisation du générateur ASCII art.

## Fichiers

- `basic_usage.py` - Exemples de base couvrant toutes les fonctionnalités principales

## Exécution des exemples

```bash
# Exécuter tous les exemples
python examples/basic_usage.py
```

## Exemples couverts

1. **Conversion de texte** - Texte simple, avec couleur, bannières
2. **Conversion d'images** - Images avec différentes palettes
3. **Palettes multiples** - Comparaison de différentes palettes
4. **Effets artistiques** - Stippling, halftone, etc.
5. **Effets de texte** - Gradients, ombres
6. **Export** - HTML et SVG
7. **Palettes personnalisées** - Création de palettes sur mesure

## Créer vos propres exemples

Vous pouvez créer vos propres scripts en important les modules:

```python
from ascii_generator import ImageToASCII, TextToASCII
from ascii_generator.palettes import CharacterPalettes

# Votre code ici
```
