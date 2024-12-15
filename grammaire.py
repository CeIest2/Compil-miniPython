class Token:
    # un token pourra être un terminal ou un non terminal, il n'aura pas alors accès aux mêmes
    # méthodes , puisque le NT aura des Premiers, des suivants ...

    def __init__(self,type_token, identificateur):
        self.type_token     = type_token              # peut être terminal ou non terminal
        self.name           = self._crea_name(identificateur)    # son nom si c'est un non_terminal et son num si c'est un terminal 
        self.representation = None    # utiliser lors du print pour pouvoir débuguer plus facilement
        self.suivant        = None

    def _crea_name(self, identificateur):
        if self.type_token == "non_terminal":
            return identificateur
        else:
            if identificateur.isdigit():
                return int(identificateur)
            else:
                return identificateur
            

class Grammaire:

    # Dans cette classe on va stocker notre grammaire et implémenter différentes méthode pour 
    # utiliser facilement cette dernière

    def __init__(self, fichier_regles):
        self.axiome        = None
        self.int_to_token  = {1: "+", 2: "-", 3: "*", 4: "/", 5: ":", 6: "%", 9: "if", 10: "then", 12: "<", 13: ">", 14: "(", 15: ")", 16: "[", 17: "]", 19: "not", 20: "def", 21: "or", 22: "and", 23: "<=", 24: ">=", 25: "==", 26: "!=", 27: "True", 28: "False", 29: "None", 30: "//", 31: ",", 32: "for", 33: "in", 34: "print", 35: "return", 36: "BEGIN", 37: "END", 38: "NEWLINE", 39: "EOF", 40: "identifiant", 41: "char", 42: "number", 43: "=", 44: "else"}
        self.regles        = self.init_regles(fichier_regles)
        self.non_terminaux = self.init_non_terminaux()
        self.premiers      = self.calculer_premiers()
        self.suivants      = self.calculer_suivants()
        


    def __str__(self):
        """
        print(grammaire)
        """
        resultat = "Grammaire :\n"
        
        # Pour chaque non-terminal dans les règles
        for non_terminal, productions in self.regles.items():
            size_skip = len(non_terminal) + 1
            space = " " * size_skip
            lignes = [f"{non_terminal} -> {' '.join(p.name if p.type_token == 'non_terminal' or p.name == '^' else self.int_to_token[int(p.name)] for p in productions[0])}"]
            
            for production in productions[1:]:
                lignes.append(f"{space}-> {' '.join(p.name if p.type_token == 'non_terminal' or p.name == '^' else self.int_to_token[int(p.name)] for p in production)}")            
            resultat += "\n".join(lignes) + "\n"
        
        return resultat.rstrip()


    def init_regles(self, fichier_regles) -> dict:
        axiome = True  # variable to set the axiom
        
        regles = {}
        
        def est_terminal(element):
            # Check if an element is a terminal
            if element.isdigit(): 
                return True
            
            # Handle tuple-like terminals (n,m)
            if (element.startswith('(') and element.endswith(')') and
                len(element.split(',')) == 2):
                try:
                    n1 = element.strip('()').split(',')[0].strip()
                    n2 = element.strip('()').split(',')[1].strip()
                    return n1.isdigit() and n2.isdigit()
                except:
                    return False
            
            # Non-terminals are enclosed in <>
            return not (element.startswith('<') and element.endswith('>'))
        
        with open(fichier_regles, 'r') as fichier:
            for ligne in fichier:
                # Separate left and right parts of the rule
                parties = ligne.strip().split('->')
                
                non_terminal = parties[0].strip()

                
                production = []
                for element in parties[1].strip().split():
                    if est_terminal(element):
                        new_token = Token("terminal", element.replace(" ", ""))
                    else:
                        new_token = Token("non_terminal", element.replace(" ", ""))
                    production.append(new_token)
                
                regles.setdefault(non_terminal, []).append(production)
                if axiome: 
                    self.axiome, axiome = [Token("non_terminal", parties[0].replace(" ",""))] ,False
         
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
        

class TableAnalyse:
    def __init__(self, grammaire):
        self.grammaire = grammaire
        self.table = self._construire_table()
        
    def _construire_table(self):
        table = {}
        
        # Initialiser la table
        for nt in self.grammaire.non_terminaux:
            
            table[nt] = {}
        
        # Remplir la table
        for nt, productions in self.grammaire.regles.items():
            for production in productions:
                if production[0].name == '^':
                    for suivant in self.grammaire.suivants[nt]:
                        
                        table[nt][suivant] = production                    

                # Si la production commence par un terminal
                elif production[0].type_token == "terminal":
                    table[nt][production[0].name] = production
                    
                # Si la production commence par un non-terminal
                elif production[0].type_token == "non_terminal":

                    for terminal in self.grammaire.premiers[production[0].name]:
                        table[nt][terminal] = production
            
        return table



if __name__ == '__main__':
    grammaire_test = Grammaire('Grammaire PCL.txt')
    print(grammaire_test)
    print("#######################")
    print(f"Les premiers de la grammaire : {grammaire_test.premiers}\nLes suivants de la grammaire : {grammaire_test.suivants}")
    print("#######################")

    table_analyse = TableAnalyse(grammaire_test)
    print(table_analyse)
    print("#######################")
    # si on a un non terminal E et que l'on lis le caractère correpondant on token 48 alors le token suivant l'unité lexical suivante doit être T  
    print(table_analyse.table['<expr>']['40'][0].name)

    # si on a un non termianl TP et que on lis 42 alors l'unité suivante doit être 42 
    print(table_analyse.table['<expr2>']['16'][0].name)


