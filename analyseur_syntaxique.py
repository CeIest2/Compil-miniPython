from grammaire import *
import analyseur_lexical as analex
from arbre_classe import Arbre, visualize_ast

def analyse_syntaxique(liste_token):
    grammaire = Grammaire("docs/Grammaire_PCL.txt")

    table_analyse = TableAnalyse(grammaire)
    # Pile de parsing
    pile = [grammaire.axiome[0]]
    liste_token_test = liste_token
    
    cara_ind = 0
    liste_token_a_afficher = [[liste_token_test.liste_token[i], grammaire.int_to_token[liste_token_test.liste_token[i]]] 
       if isinstance(liste_token_test.liste_token[i], int) 
       else liste_token_test.liste_token[i] 
       for i in range(len(liste_token_test.liste_token))]
    for _ in range(len(liste_token_a_afficher)//10+1):
        print(liste_token_a_afficher[_*10:(_+1)*10])

    while pile:
        print([ token.name for token in pile])

        # cas de lecture d'un termianle au début de la pile
        if pile[-1].type_token == "terminal":
            #on va lire un caractère du fichier et le comparer à la pile
            cara = liste_token_test.liste_token[cara_ind]
            print(f"{cara = }")
            if isinstance(cara, int):
                if pile[-1].name == cara:
                    print(f"{pile.pop().name = }")
                    cara_ind += 1
                else:
                    print("Erreur de syntaxe ")
                    print(f"ce qu'on la grammaire coudrais : {pile[-1].name} et ce que l'on a : {cara}")
                    print(f"nb token qui a chier : {cara_ind}")
                    print(f"""premiers {table_analyse.grammaire.premiers["<expr2>"]}""")
                    break
            else:
                if pile[-1].name == cara[0]:
                    print(f"{pile.pop().name = }")
                    cara_ind += 1
                else:
                    print("Erreur de syntaxe ")
                    print(f"ce qu'on la grammaire coudrais : {pile[-1].name} et ce que l'on a : {cara}")
                    print(f"nb token qui a chier : {cara_ind}")
                    break
            
        # cas de lecture d'un non termianl au début de la pile
        elif pile[-1].type_token == "non_terminal":
            #on va chercher la production dans la table d'analyse syntaxique
            
            # il faut qu'on regard si c'est un token int ou un token tuple qui est le suivant à être lu
            if isinstance(liste_token_test.liste_token[cara_ind], int):
                #on est dans le cas d'in token de int
                cara_suivant = liste_token_test.liste_token[cara_ind]
                print(f"{cara_suivant = }")
                
            else:
                #on est dans le cas d'un token de tuple
                cara_suivant = liste_token_test.liste_token[cara_ind][0]
                print(f"{cara_suivant = }")            
            
            
            try:
                production = table_analyse.table[pile[-1].name][cara_suivant]
                if pile[-1].name == "<expr2>":
                    print(f"production {production[0].name}")
            except :
                if cara_suivant == 39:

                    print("affection d'une variable qui n'est pas utiliser à la dernière ligne")
                    print(f" suivants de {pile[-1].name} {table_analyse.grammaire.suivants[pile[-1].name] }")
                    print(f" suivants de {pile[-2].name} {table_analyse.grammaire.suivants[pile[-1].name] }")
                    print(f" premiers de {pile[-1].name} {table_analyse.grammaire.premiers[pile[-1].name] }")
                    print(f" premiers de {pile[-2].name} {table_analyse.grammaire.premiers[pile[-1].name] }")
                else:
                    print(f" caractère que l'on a {liste_token_test.liste_token[cara_ind]}")
                    print(f" caractère que le compilateur aurait aimer avoir {pile[-1].name}")
                    print(f" table analyse {table_analyse.table[pile[-1].name]}")
                    
                break

            if production:
                pile.pop()
                if production[0].name != "^":
                    for symbol in reversed(production):
                        pile.append(symbol)
            else:
                print("Erreur de syntaxe 57")
                break

    print(cara_ind)
    print(liste_token.liste_token[cara_ind:])
    return -1,-1




if __name__ == '__main__':
    liste_token = analex.analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    print(liste_token.liste_token)
    arbre_derivation, message_erreur = analyse_syntaxique(liste_token)