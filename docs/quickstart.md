# Guide de Démarrage Rapide LOKA

## Installation

```bash
pip install loka
```

## Premier Programme

```loka
# Mon premier programme LOKA
fonction main() {
    affiche("Bonjour depuis LOKA!")
}
```

## Opérations de Base

### Variables et Types
```loka
# Types de base
x = 42          # Nombre
texte = "LOKA"  # Chaîne
liste = [1, 2, 3]  # Liste
```

### Mathématiques
```loka
# Opérations mathématiques
a = 10
b = 5

somme = a + b
difference = a - b
produit = a * b
quotient = a / b
```

### Affichage
```loka
# Affichage de résultats
affiche("Résultat:", resultat)
affiche("x =", x)
```

## Exemple IA Simple

```loka
# Classification simple
fonction classifier_image(image) {
    # Prétraitement
    features = extraire_features(image)
    
    # Prédiction
    prediction = modele.predire(features)
    
    affiche("Classe prédite:", prediction)
}
```

## Bonnes Pratiques

1. Toujours définir une fonction `main()`
2. Utiliser des noms descriptifs
3. Commenter le code
4. Gérer les erreurs

## Ressources

- Documentation complète : `/docs/documentation.md`
- Exemples : `/examples/`
- Tutoriels : `/tutorials/`

## Support

Pour toute question ou assistance :
- Email : contact@loka-lang.org
- Forum : forum.loka-lang.org
- GitHub : github.com/loka-lang

---

© 2025 ALLE OSSEY ANGE CEDRIC - Tous droits réservés
