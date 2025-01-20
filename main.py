import analyseur_lexical2 as analex
import analyseur_syntaxique as anasyn

def analyseur(code_entré):
    """
        cette fonction a pour bute de créer l'arbre syntaxique et d'afficher ce dernier 
    """

    liste_token, analyse_lexical = analex.analyseur(code_entré)

    if  not analyse_lexical:
        print("dommage ça compile pas")
        exit()

    arbre_derivation = anasyn.analyse_syntaxique(liste_token)


    #arbre_abstrait = fonction_pour_faire_AST(arbre_derivation)

    # affichage de l'abre
    

    

if __name__ == "__main__":
    code_entré = ".fichier_test/fichier_test_lexeur/mini_test.txt"
    analyseur(code_entré)