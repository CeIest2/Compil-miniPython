from grammaire import *
import analyseur_lexical2 as analex
from arbre import ASTNode, visualize_ast

def analyse_syntaxique(liste_token):
    grammaire = Grammaire("docs/Grammaire_PCL.txt")

    table_analyse = TableAnalyse(grammaire)
    liste_token_test = analex.analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    # Pile de parsing
    pile = [grammaire.axiome[0]]
    cara_ind = 0
    print(liste_token_test.liste_token)
    while pile:

        # cas de lecture d'un termianle au début de la pile
        if pile[0].type_token == "terminal":
            #on va lire un caractère du fichier et le comparer à la pile
            cara = liste_token_test.liste_token[cara_ind]
            if pile[0].name == cara[0]:
                pile.pop(0)
                cara_ind += 1
            else:
                print("Erreur de syntaxe")
                break
        
        # cas de lecture d'un non termianl au début de la pile
        elif pile[0].type_token == "non_terminal":
            #on va chercher la production dans la table d'analyse syntaxique
            cara_suivant = str(liste_token_test.liste_token[cara_ind])
            print(cara_suivant)
            print(table_analyse.table[pile[0].name])
            print(table_analyse.table[pile[0].name][cara_suivant])

            
            production = table_analyse.table[pile[0].name][cara_suivant]

            if production:
                pile.pop(0)
                for symbol in reversed(production):
                    pile.insert(0, symbol)
            else:
                print("Erreur de syntaxe")
                break
        print(pile)

        

    return -1,-1




if __name__ == '__main__':
    liste_token = analex.analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    arbre_derivation, message_erreur = analyse_syntaxique(liste_token)