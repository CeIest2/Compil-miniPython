# Projet Compilateur Mini-Python

## Description

Ce projet est un compilateur pour un sous-ensemble du langage Python, appelé **Mini-Python**. Il permet d'analyser, de traiter et de tester des fichiers écrits dans ce langage simplifié.

Une description du langauge mini-Pyhton est disponible dans `docs/sujet.pdf`.

---

## Fonctionnalités

- Analyse lexicale des fichiers Mini-Python.
- Analyse syntaxique avec gestion des erreurs.
- Génération d'arbres syntaxiques abstraits (AST).
- Tests automatisés sur des fichiers `.mpy`.

---

## Structure du Projet

Voici la structure des dossiers et fichiers principaux du projet :

```
.
├── analyseur_lexical.py         # Analyseur lexical
├── analyseur_syntaxique.py      # Analyseur syntaxique
├── arbre_classe.py                     # classe arbre et visualisation
├── ast_utils.py                       # simplification de l'arbre
├── fichier_test/                # Dossier contenant les fichiers de test
│   ├── fichier_test_1.mpy
│   └── ...
├── lancer_test.py               # Script pour lancer les tests
├── main.py                      # Point d'entrée principal du projet (execution de 1 test)
└── docs/                        # Documentation
    ├── Analyseur_lex.txt
    └── ...
```

---

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/votre-projet.git
   cd votre-projet
   ```

2. Assurez-vous que Python est installé :
   ```bash
   python3 --version
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## Utilisation

### Lancer les tests
Pour exécuter les tests sur tous les fichiers dans le dossier `fichier_test` :
```bash
python3 lancer_test.py
```
ou pour exécuter 1 seul fichier test
```bash
python3 main.py <chemin-du-fichier>
```

---

## Auteurs

- **Célestin Morel**
- **David Guichard**
- **Romain Samba**
- **Livie Romanet**

---

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

