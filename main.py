import analyseur_lexical2 as analex
import analyseur_syntaxique as anasyn

def analyseur(code_entré):
    """
        cette fonction a pour bute de créer l'arbre syntaxique et d'afficher ce dernier 
    """

    liste_token, reussite_compilation = analex.analyseur(code_entré)

    if  not reussite_compilation:
        print("dommage ça compile pas")
        exit()

    arbre_derivation = anasyn.analyse_syntaxique(liste_token)


    #arbre_abstrait = fonction_pour_faire_AST(arbre_derivation)

    # affichage de l'abre
    

    

