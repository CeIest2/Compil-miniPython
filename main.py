import analyseur_lexical2 as analex
import analyseur_syntaxique_ss_erreru as anasyn
import ast_1 as ast_const
import arbre 


def analyseur(code_entré,visualisation = True):
    """
        cette fonction a pour bute de créer l'arbre syntaxique et d'afficher ce dernier 
    """
    print("nifdsnoqvsdojd")
    liste_token = analex.analyseur(code_entré)

    if  -1 in liste_token.liste_token:
        print(liste_token.message_erreur)
        return -1
    print("jofdsoqfdsqjf")
    arbre_derivation, erreur = anasyn.analyse_syntaxique(liste_token)
    if erreur != None:
        print("Erreur syntaxique")
        return -1
    print("nojodfpnjodsfpnvsq")
    ast = ast_const.simplify_tree(arbre_derivation)
    if visualisation:
        arbre.visualize_ast(ast)

    return 1
    
    

    

if __name__ == "__main__":
    code_entré = "fichier_test/fichier_test_7.mpy"
    analyseur(code_entré)