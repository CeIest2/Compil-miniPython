# Projet Compilateur Mini-Python

## Description

Ce projet est un compilateur pour un sous-ensemble du langage Python, appelé **Mini-Python**. Il permet d'analyser, de traiter et de tester des fichiers écrits dans ce langage simplifié.

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
├── arbre.py                     # classe arbre et visualisation
├── ast.py                       # simplification de l'arbre
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

### Ajouter de nouveaux fichiers de test
Pour lancer la compilation d'un nouveau fichier `new_fichier.mpy`:
   ```bash
   python3 main.py new_fichier.mpy
   ```

---

## Contribuer

Les contributions sont les bienvenues ! Suivez ces étapes pour contribuer au projet :

1. Forkez ce dépôt.
2. Créez une branche pour votre fonctionnalité :
   ```bash
   git checkout -b nouvelle-fonctionnalite
   ```
3. Faites vos modifications et commitez-les :
   ```bash
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   ```
4. Poussez vos modifications :
   ```bash
   git push origin nouvelle-fonctionnalite
   ```
5. Ouvrez une pull request.

---

## Auteurs

- **Célestin Morel**
- **David Guichard**
- **Romain Samba**
- **Livie Romanet**

---

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

