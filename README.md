# LOKA - Un langage de programmation moderne pour l'IA

![PyPI Version](https://img.shields.io/pypi/v/loka-lang.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

LOKA est un langage de programmation moderne conçu pour être plus facile que Python et plus performant que C++, spécialement optimisé pour l'IA et le machine learning.

## 🚀 Installation

```bash
pip install loka-lang
```

## 📖 Guide d'utilisation

### Syntaxe de base

LOKA supporte deux syntaxes : française et anglaise. Voici les mots-clés principaux :

| Français  | English   | Description                    |
|-----------|-----------|--------------------------------|
| fonction  | function  | Définir une fonction           |
| classe    | class     | Définir une classe             |
| si        | if        | Condition                      |
| sinon     | else      | Alternative                    |
| pour      | for       | Boucle                         |
| tant que  | while     | Boucle conditionnelle          |
| retourne  | return    | Retourner une valeur           |
| affiche   | print     | Afficher dans la console       |

### Exemples de base

#### Hello World
```loka
fonction main() {
    affiche("Bonjour depuis LOKA!")
}
```

#### Calculs mathématiques
```loka
fonction calculer(x, y) {
    retourne x * y + 100
}

fonction main() {
    resultat = calculer(5, 10)
    affiche("Le résultat est : " + resultat)
}
```

### 🧮 Opérations Matricielles

LOKA intègre nativement le support des opérations matricielles via NumPy :

```loka
# Création et manipulation de matrices
fonction matrices_exemple() {
    # Créer une matrice 2x2
    A = matrice([[1, 2], [3, 4]])
    B = matrice([[5, 6], [7, 8]])
    
    # Multiplication matricielle
    C = A * B
    
    affiche("Résultat : " + C)
}
```

### 🤖 Intelligence Artificielle

LOKA facilite l'intégration avec les bibliothèques d'IA :

```loka
# Classification simple
fonction classification() {
    # Charger les données
    donnees = charger_donnees("data.csv")
    
    # Créer et entraîner un modèle
    modele = ClassifieurIA()
    modele.entrainer(donnees.X, donnees.y)
    
    # Prédire
    predictions = modele.predire(donnees.X_test)
    affiche("Précision : " + modele.precision)
}
```

### 🏗️ Programmation Orientée Objet

```loka
classe Voiture {
    fonction constructeur(marque, modele) {
        this.marque = marque
        this.modele = modele
    }
    
    fonction description() {
        retourne "Voiture " + this.marque + " " + this.modele
    }
}

fonction main() {
    maVoiture = Voiture("Renault", "Clio")
    affiche(maVoiture.description())
}
```

## 📂 Structure des fichiers LOKA

- Les fichiers LOKA utilisent l'extension `.loka`
- Un fichier peut contenir plusieurs classes et fonctions
- La fonction `main()` est le point d'entrée du programme

## 🛠️ Exécution des programmes

Pour exécuter un fichier LOKA :

```bash
python -m loka mon_programme.loka
```

## 🔍 Débogage

LOKA inclut des outils de débogage intégrés :

```loka
fonction debug_exemple() {
    # Active le mode debug
    debug.activer()
    
    # Affiche les variables
    x = 42
    debug.afficher(x)
    
    # Désactive le mode debug
    debug.desactiver()
}
```

## 🎯 Cas d'usage

### 1. Analyse de données
```loka
fonction analyser_donnees(fichier) {
    donnees = charger_csv(fichier)
    stats = donnees.statistiques()
    graphique = donnees.visualiser()
    
    affiche("Moyenne : " + stats.moyenne)
    affiche("Écart-type : " + stats.ecart_type)
    
    graphique.sauvegarder("resultats.png")
}
```

### 2. Apprentissage automatique
```loka
fonction entrainer_modele() {
    # Préparation des données
    donnees = preparer_donnees()
    
    # Création du modèle
    modele = ReseauNeuronal([
        Couche(128, "relu"),
        Couche(64, "relu"),
        Couche(10, "softmax")
    ])
    
    # Entraînement
    modele.entrainer(donnees, epochs=10)
    
    # Évaluation
    precision = modele.evaluer(donnees.test)
    affiche("Précision : " + precision)
}
```

## 📚 Ressources supplémentaires

- [Documentation complète](https://loka-lang.readthedocs.io/)
- [Tutoriels vidéo](https://youtube.com/loka-lang)
- [Forum communautaire](https://github.com/cedric202012/loka/discussions)

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez notre guide de contribution pour commencer.

## 📄 Licence

LOKA est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus de détails.
