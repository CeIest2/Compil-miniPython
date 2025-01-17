from grammaire import *
import analyseur_lexical2 as analex
from arbre import ASTNode, visualize_ast

def analyse_syntaxique(liste_token):
    grammaire = Grammaire("docs/Grammaire_PCL.txt")
    table_analyse = TableAnalyse(grammaire)
    # Pile de parsing
    pile = [grammaire.axiome[0]]
    # Pile des nœuds pour construire l'arbre
    pile_noeuds = [ASTNode(grammaire.axiome[0].name)]
    liste_token_test = liste_token

    cara_ind = 0
    arbre = pile_noeuds[0]  # La racine de l'arbre

    while pile:
        sommet_pile = pile[-1]
        noeud_parent = pile_noeuds[-1]

        # Cas de lecture d'un terminal au début de la pile
        if sommet_pile.type_token == "terminal":
            cara = liste_token_test.liste_token[cara_ind]
            if isinstance(cara, int):
                if sommet_pile.name == cara:
                    # Ajouter le terminal comme fils
                    noeud_parent.add_child(ASTNode(sommet_pile.name))
                    cara_ind += 1
                else:
                    print("Erreur syntaxique : terminal inattendu.")
                    break
            else:
                if sommet_pile.name == cara[0]:
                    # Ajouter le terminal comme fils
                    noeud_parent.add_child(ASTNode(sommet_pile.name))
                    cara_ind += 1
                else:
                    print("Erreur syntaxique : terminal inattendu.")
                    break
            pile.pop()
            pile_noeuds.pop()

        # Cas de lecture d'un non-terminal au début de la pile
        elif sommet_pile.type_token == "non_terminal":
            if isinstance(liste_token_test.liste_token[cara_ind], int):
                cara_suivant = liste_token_test.liste_token[cara_ind]
            else:
                cara_suivant = liste_token_test.liste_token[cara_ind][0]

            try:
                production = table_analyse.table[sommet_pile.name][cara_suivant]
            except KeyError:
                print("Erreur de syntaxe : Production introuvable.")
                break

            if production:
                pile.pop()
                pile_noeuds.pop()
                if production[0].name != "^":
                    for symbol in reversed(production):
                        if symbol.type_token == "non_terminal":
                            new_node = ASTNode(symbol.name)
                            noeud_parent.add_child(new_node)
                            pile.append(symbol)
                            pile_noeuds.append(new_node)
                        else:  # terminal
                            pile.append(symbol)
                            pile_noeuds.append(noeud_parent)
                else:
                    # Cas où la production contient uniquement "^" (epsilon)
                    noeud_parent.add_child(ASTNode("^"))
            else:
                print("Erreur de syntaxe : Production invalide.")
                break

    # Vérification de la fin de l'analyse
    if cara_ind == len(liste_token.liste_token) and not pile:
        print("Analyse syntaxique réussie.")
        return arbre, None
    else:
        print("Erreur de syntaxe : Analyse incomplète.")
        return None, "Erreur de syntaxe"


if __name__ == '__main__':
    liste_token = analex.analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    print(liste_token.liste_token)
    arbre_derivation, message_erreur = analyse_syntaxique(liste_token)

    if arbre_derivation:
        visualize_ast(arbre_derivation)
