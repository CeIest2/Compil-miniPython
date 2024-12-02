# Documentation - Classes `Token` et `Grammaire`
## Classe `Token`

Cette classe représente un token qui peut être soit un terminal, soit un non-terminal. Elle est utilisée pour modéliser les éléments de la grammaire.
### Attributs

    type_token : Indique le type du token ("terminal" ou "non_terminal").
    name : Identificateur du token (nom pour les non-terminaux, numéro ou symbole pour les terminaux).
    representation : (Optionnel) Une représentation lisible pour le débogage.
    suivant : (Optionnel) Ensemble des suivants associés au token (utilisé pour les non-terminaux).

### Méthodes

    init_representation : Initialise une représentation textuelle du token (non implémentée actuellement).

## Classe `Grammaire`

Cette classe sert à stocker et manipuler une grammaire formelle. Elle fournit des outils pour travailler sur les règles de grammaire, les ensembles des premiers et suivants des non-terminaux, et pour vérifier les propriétés de la grammaire.
### Attributs

    regles dict[str] : List[List[Token]] : Un dictionnaire où les clés sont des non-terminaux et les valeurs sont des listes de productions. Chaque production est une liste de Token.
    non_terminaux List[str] : Ensemble des non-terminaux présents dans la grammaire.
    premiers dict[str] : set(str) : Dictionnaire associant chaque non-terminal à son ensemble de premiers.

### Méthodes


    __init__(self, fichier_regles) : Charge les règles depuis un fichier et initialise les attributs principaux.



    __str__(self) : Retourne une représentation textuelle de la grammaire, listant chaque non-terminal et ses productions. C'est pour faire print(grammaire)


    init_regles(self, fichier_regles) : Lit les règles de grammaire depuis un fichier et les stocke dans le dictionnaire regles.



    init_non_terminaux(self) : Identifie et retourne l'ensemble des non-terminaux présents dans la grammaire.



    calculer_premiers(self) : Calcule l'ensemble des premiers pour chaque non-terminal de la grammaire.

## Utilisation

    Créez une instance de Grammaire en passant le chemin d'un fichier contenant les règles de grammaire :

grammaire = Grammaire('grammaire.txt')

Affichez la grammaire :

    print(grammaire)

    Les ensembles des premiers sont calculés automatiquement à l'initialisation et accessibles via grammaire.premiers.

## Exemple de fichier de grammaire

Le fichier grammaire.txt doit suivre la syntaxe suivante :

E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | id

Chaque règle est écrite sous la forme NonTerminal -> production1 | production2 ..., où les productions sont séparées par des espaces.

Cette documentation peut être enrichie avec des explications sur les cas particuliers comme les règles vides (ε) ou les terminaux spéciaux (EOF, etc.).