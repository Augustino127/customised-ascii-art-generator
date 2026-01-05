# Guide de Contribution

Merci de votre intérêt pour contribuer au Générateur ASCII Art !

## Comment Contribuer

### Signaler des Bugs

1. Vérifiez que le bug n'a pas déjà été signalé dans les Issues
2. Créez une nouvelle Issue avec:
   - Description claire du problème
   - Étapes pour reproduire
   - Résultat attendu vs résultat obtenu
   - Version Python et système d'exploitation

### Proposer des Fonctionnalités

1. Ouvrez une Issue pour discuter de la fonctionnalité
2. Expliquez le cas d'usage et les bénéfices
3. Attendez les retours avant de commencer l'implémentation

### Soumettre des Pull Requests

1. **Fork** le repository
2. **Créez une branche** pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`)
3. **Commitez** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. **Testez** votre code (`python tests/test_basic.py`)
5. **Pushez** vers votre branche (`git push origin feature/ma-fonctionnalite`)
6. **Ouvrez une Pull Request**

## Standards de Code

### Style Python

- Suivre PEP 8
- Utiliser des docstrings pour toutes les fonctions publiques
- Ajouter des type hints quand possible

### Tests

- Ajouter des tests pour toute nouvelle fonctionnalité
- S'assurer que tous les tests passent avant de soumettre

```bash
python tests/test_basic.py
```

### Documentation

- Mettre à jour le README si nécessaire
- Documenter les nouvelles fonctionnalités
- Ajouter des exemples d'utilisation

## Structure du Projet

```
ascii_generator/
├── core/           # Moteurs de conversion
├── effects/        # Effets artistiques
├── exporters/      # Exporteurs multi-formats
├── palettes/       # Palettes et styles
└── cli/           # Interface CLI
```

## Processus de Review

1. Un mainteneur reviewera votre PR
2. Des changements peuvent être demandés
3. Une fois approuvée, la PR sera mergée

## Questions ?

N'hésitez pas à ouvrir une Issue pour poser des questions !

## Code de Conduite

Soyez respectueux et constructif dans vos interactions.

---

Merci pour vos contributions !
