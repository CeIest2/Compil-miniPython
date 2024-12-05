# Documentation - Classes 

## Classe `Liste_token`

Classe qui représente la liste de token en sortie de l'analyseur lexical

### Attributs


        dico_idf       : dictionnaire des différents identifiants  les clés sont les int et les valeur sont les identifiants en toute lettres
        nb_identifiant : nombre d'indentifiants différents
        dico_char      : dictionnaire des chaînes de caractères, même fonctinonement que dico_idf
        nb_char        : ''
        dico_number    : ''
        nb_number      : ''
        dict_lexique   : dictionnaire mot de la grammaire -> int de token 

### Utilisation

Dans le code on utilise cette classe d'abors dans l anaylseur lexical ou on construit un objet Liste_token du code à compiler.
Puis dans l'analyseur syntaxique on pourra :

```python
liste_token, erreur = analyseur("fichier_a_analyser.txt")
# pour avoir la liste des token :
liste_token.liste_token
# pour avoir le dictionnaire des identificateurs :
liste_token.dico_idf
# ...
liste_token.dico_char
# ...
liste_token.dico_nb
```


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

    init_regles(self, fichier_regles) 
Lit les règles de grammaire depuis un fichier et les stocke dans le dictionnaire regles.



    init_non_terminaux(self)
Identifie et retourne l'ensemble des non-terminaux présents dans la grammaire.



    calculer_premiers(self)
Calcule l'ensemble des premiers pour chaque non-terminal de la grammaire.

## Utilisation

    Créez une instance de Grammaire en passant le chemin d'un fichier contenant les règles de grammaire :

grammaire = Grammaire('grammaire.txt')

Affichez la grammaire :

    print(grammaire)

Les ensembles des premiers sont calculés automatiquement à l'initialisation et accessibles via grammaire.premiers.

## Exemple de fichier de grammaire

Le fichier grammaire.txt doit suivre la syntaxe suivante :

    <E> -> <T> <E'>
    <E'> -> + <T> <E'> 
    <E'> -> ^
    <T> -> <F> <T'>
    <T'> -> * <F> <T'> 
    <T'> -> ^
    <F> -> ( <E> )
    <F> -> ^

Chaque règle est écrite sous la forme NonTerminal -> production1 | production2 ..., où les productions sont séparées par des espaces.

Cette documentation peut être enrichie avec des explications sur les cas particuliers comme les règles vides (ε) ou les terminaux spéciaux (EOF, etc.).