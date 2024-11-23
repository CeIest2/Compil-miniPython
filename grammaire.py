class Token:
    # un token pourra être un terminal ou un non terminal, il n'aura pas alors accès aux mêmes
    # méthodes , puisque le NT aura des Premiers, des suivants ...

    def __init__(self,type_token, identificateur):
        self.type_token     = type_token              # peut être terminal ou non terminal
        self.name           = identificateur    # son nom si c'est un non_terminal et son num si c'est un terminal 
        self.representation = None    # utiliser lors du print pour pouvoir débuguer plus facilement
        self.suivant        = None

    def init_representation(self):

        #TODO faire une fonction  faire une fonction pour pouvoir afficher de puis un numéro de token mais pour l instant flemme et on a déjà ça dans le fichier analyseur_lexical2.py
        """
        def ent_to_terminal(entier):
            dico_terminal_ent = {"+" : 1,"-" : 2,"*" : 3,"/" : 4,":" : 5,"%" : 6,"if" : 9,"then" : 10,"<" : 12,">" : 13,"(" : 14,")" : 15,"[" : 16,"]" : 17,"not" : 19,"def" : 20,"or" : 21,"and" : 22,"<=" : 23,">=" : 24,"==" : 25,"!=" : 26,"True" : 27,"False" : 28,"None" : 29,"//" : 30,"," : 31,"for" : 32,"in" : 33,"print" : 34,"return" : 35,"BEGIN" : 36,"END" : 37,"NEWLINE" : 38,"EOF" : 39, "identifiant" : 40, "char" : 41, "number":42, "=": 43}
            if 
        
        if self.type == "terminal": self.representation = self.name
        elif self.type == "non_terminale": 
        """
        pass
            

class Grammaire:

    # Dans cette classe on va stocker notre grammaire et implémenter différentes méthode pour 
    # utiliser facilement cette dernière

    def __init__(self, fichier_regles):
        self.axiome = None
        self.regles = self.init_regles(fichier_regles)
        print(self)
        self.non_terminaux = self.init_non_terminaux()
        self.premiers = self.calculer_premiers()
        self.suivants = self.calculer_suivants()
        


    def __str__(self):
        """
        print(grammaire)
        """
        resultat = "Grammaire :\n"
        
        # Pour chaque non-terminal dans les règles
        for non_terminal, productions in self.regles.items():
            lignes = [f"{non_terminal} -> {' '.join(p.name for p in productions[0])}"]
            
            for production in productions[1:]:
                lignes.append(f"  -> {' '.join(p.name for p in production)}")
            
            resultat += "\n".join(lignes) + "\n"
        
        return resultat.rstrip()


    def init_regles(self, fichier_regles):
        axiome = True # variable qui sert pour def l axiome
        
        regles = {}

        def est_terminal(element):
            if element.isdigit(): return True  
            
            # Cas d'un tuple (n,m)
            if (element.startswith('(') and element.endswith(')') and 
                len(element.split(',')) == 2):
                try:
                    n1 = element.strip('()').split(',')[0].strip()
                    n2 = element.strip('()').split(',')[1].strip()
                    return n1.isdigit() and n2.isdigit()
                except:
                    return False
            return False

        with open(fichier_regles, 'r') as fichier:
            for ligne in fichier:
                

                # Séparer la partie gauche et droite de la règle
                parties = ligne.strip().split('->')
                    
                non_terminal = parties[0].strip()
                if axiome: self.axiome,axiome = non_terminal, False
                production = []
                for element in parties[1].strip().split():
                    if est_terminal(element):
                        new_token = Token("terminal", element)
                    else:
                        new_token = Token("non_terminal", element)
                    production.append(new_token)
               
                regles.setdefault(non_terminal, []).append(production)
        return regles

        


    def init_non_terminaux(self):
        non_terminaux = set()
        for non_terminal in self.regles.keys():
            if non_terminal not in non_terminaux:
                non_terminaux.add(non_terminal)
        return non_terminaux

    
    
    
    def calculer_premiers(self):
        premiers = {non_terminal: set() for non_terminal in self.non_terminaux}

        def premiers_de(non_terminal, regles):
            premiers_local = set()  # Utiliser un set pour éviter les doublons

            for regle in regles:
                for element in regle:
                    if element.type_token == "terminal":
                        # Ajouter directement le terminal
                        premiers_local.add(element.name)
                        break
                    elif element.type_token == "non_terminal":
                        if element.name == '^':
                            premiers_local.add('^')
                            break
                        premiers_local.update(premiers_de(element.name, self.regles[element.name]))

                        # Si le non-terminal ne produit pas vide, arrêter
                        if '^' in premiers_local:
                            premiers_local.remove('^')
                        else:
                            break
                else:
                    premiers_local.add('^')
            return premiers_local
                        
        for nt, regles in self.regles.items():
            premiers[nt] = premiers_de(nt,regles)
            if "^" in premiers[nt]:
                premiers[nt].remove("^")
        return premiers
                    
    def calculer_suivants(self):
        suivants = {non_terminal: set() for non_terminal in self.non_terminaux}

        suivants[self.axiome].add('39')  # <EOF> est représenté par '39'

        def suivants_de(non_terminal):
            suivants_local = suivants[non_terminal]  # Récupérer les Suivants existants du non-terminal

            for nt, regles in self.regles.items():
                for regle in regles:
                    for i, element in enumerate(regle):
                        if element.type_token == "non_terminal" and element.name == non_terminal:
                            # Regarder les éléments après `element` dans la règle
                            for suivant in regle[i + 1:]:
                                if suivant.type_token == "terminal":
                                    # Ajouter directement le terminal
                                    suivants_local.add(suivant.name)
                                    break
                                elif suivant.type_token == "non_terminal":
                                    # Ajouter Premiers(suivant), sans '^'
                                    suivants_local.update(self.premiers[suivant.name] - {'^'})
                                    if '^' not in self.premiers[suivant.name]:
                                        break
                            else:
                                # Si on atteint la fin de la règle, ajouter Suivants(nt)
                                suivants_local.update(suivants[nt])
            return suivants_local

        # Propagation des Suivants jusqu'à stabilisation
        changement = True
        while changement:
            changement = False
            for nt in self.non_terminaux:
                taille_avant = len(suivants[nt])
                suivants[nt] = suivants_de(nt)
                if len(suivants[nt]) > taille_avant:
                    changement = True
        return suivants
        


if __name__ == '__main__':
    grammaire_test = Grammaire('grammaire.txt')
    print(f"Les premiers de la grammaire : {grammaire_test.premiers}\nLes suivants de la grammaire : {grammaire_test.suivants}")


