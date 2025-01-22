import analyseur_lexical2 as analex
import analyseur_syntaxique_ss_erreru as anasyn
import ast_1 as ast_const
import arbre
import sys

def analyseur(code_entré, visualisation=True):
    """
    Cette fonction a pour but de créer l'arbre syntaxique et d'afficher ce dernier
    """
    liste_token = analex.analyseur(code_entré)
    if -1 in liste_token.liste_token:
        liste_token.afficher_erreurs()
        return -1
    
    arbre_derivation, erreur = anasyn.analyse_syntaxique(liste_token)
    if erreur is not None:
        print("Erreur syntaxique")
        return -1
    
    ast = ast_const.ast_final(arbre_derivation)
    if visualisation:
        arbre.visualize_ast(ast)
    return 1

if __name__ == "__main__":
    # Vérifier si un argument a été passé
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <chemin_vers_fichier>")
        sys.exit(1)
    
    # Récupérer le chemin du fichier depuis les arguments
    chemin_fichier = sys.argv[1]
    
    # Appeler l'analyseur avec le fichier spécifié
    resultat = analyseur(chemin_fichier)
    sys.exit(0 if resultat == 1 else 1)
