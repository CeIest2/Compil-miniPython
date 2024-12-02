from grammaire import *
import analyseur_lexical2 as analex

def analyse_syntaxique(liste_token):
    grammaire = Grammaire("docs/Grammaire\ PCL.txt")

    # la on parcoure la liste des token on forme l'anaylse sytaxique et donc l arbre de dérivation


    # on  va renvoyer un arbre de dérivation et un message d'erreur (None si la compilation c'est bien déroulé)
    #return arbre, message_erreur
    pass




if __name__ == '__main__':
    liste_token = analex.analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    arbre_derivation, message_erreur = analyse_syntaxique(liste_token)