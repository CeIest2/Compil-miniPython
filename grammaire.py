class Token:
    # un token pourra être un terminal ou un non terminal, il n'aura pas alors accès aux mêmes
    # méthodes , puisque le NT aura des Premiers, des suivants ...

    def __init__(self,type_token, identificateur):
        self.type_token     = type_token              # peut être terminal ou non terminal
        self.name           = self.__crea_name__(identificateur)    # son nom si c'est un non_terminal et son num si c'est un terminal 

    def __crea_name__(self, identificateur):
        if self.type_token == "non_terminal":
            return identificateur
        else:
            if identificateur.isdigit():
                return int(identificateur)
            else:
                return identificateur
            
    def __str__(self):
        return  f"{self.name}"
            

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
            if not premiers[non_terminal]:  # Si pas encore calculé
                for regle in regles:
                    premiers_regle = set()
                    tous_epsilon = True
                    
                    for element in regle:
                        if element.type_token == "terminal":
                            premiers_regle.add(element.name)
                            tous_epsilon = False
                            break
                        elif element.type_token == "non_terminal":
                            if element.name == '^':
                                premiers_regle.add('^')
                                break
                            # Récursion pour calculer les premiers du non-terminal
                            premiers_element = premiers_de(element.name, self.regles[element.name])
                            premiers_regle.update(premiers_element - {'^'})
                            if '^' not in premiers_element:
                                tous_epsilon = False
                                break
                    
                    if tous_epsilon:
                        premiers_regle.add('^')
                    
                    premiers[non_terminal].update(premiers_regle)
            
            return premiers[non_terminal]

        # Calculer les premiers pour tous les non-terminaux
        for nt, regles in self.regles.items():
            premiers_de(nt, regles)
        
        return premiers

    def calculer_suivants(self):
        suivants = {non_terminal: set() for non_terminal in self.non_terminaux}
        
        # Initialiser le suivant de l'axiome avec EOF
        suivants[self.axiome[0].name].add('39')  # 39 est EOF dans votre dictionnaire int_to_token
        
        def suivants_de(non_terminal):
            for nt, regles in self.regles.items():
                for regle in regles:
                    for i, element in enumerate(regle):
                        if element.type_token == "non_terminal" and element.name == non_terminal:
                            reste_regle = regle[i + 1:]
                            
                            if not reste_regle:  # Si c'est le dernier élément
                                suivants[non_terminal].update(suivants[nt])
                            else:
                                premiers_reste = set()
                                tous_epsilon = True
                                
                                for suivant in reste_regle:
                                    if suivant.type_token == "terminal":
                                        premiers_reste.add(suivant.name)
                                        tous_epsilon = False
                                        break
                                    elif suivant.type_token == "non_terminal":
                                        premiers_suivant = self.premiers[suivant.name]
                                        premiers_reste.update(premiers_suivant - {'^'})
                                        if '^' not in premiers_suivant:
                                            tous_epsilon = False
                                            break
                                
                                suivants[non_terminal].update(premiers_reste)
                                if tous_epsilon:
                                    suivants[non_terminal].update(suivants[nt])
            
            return suivants[non_terminal]

        # Propager les suivants jusqu'à stabilisation
        changement = True
        while changement:
            ancien_suivants = {nt: suivants[nt].copy() for nt in self.non_terminaux}
            
            for nt in self.non_terminaux:
                suivants_de(nt)
            
            # Vérifier s'il y a eu des changements
            changement = any(suivants[nt] != ancien_suivants[nt] for nt in self.non_terminaux)
        
        return suivants
        

class TableAnalyse:
    def __init__(self, grammaire):
        self.grammaire = grammaire
        self.table = self._construire_table()
        
    def _construire_table(self):
        table = {}
        conflits = []
        
        # Initialiser la table
        for nt in self.grammaire.non_terminaux:
            table[nt] = {}
        
        # Remplir la table
        for nt, productions in self.grammaire.regles.items():
            for production in productions:
                if production[0].name == '^':  # Production vide (ε)
                    for suivant in self.grammaire.suivants[nt]:
                        if suivant in table[nt]:
                            # Vérifier si un conflit existe
                            conflit_regle = table[nt][suivant]
                            if conflit_regle[0].name != '^':  # Préférer les règles non vides
                                continue  # Ne pas insérer cette règle
                        table[nt][suivant] = production
                
                elif production[0].type_token == "terminal":
                    if production[0].name in table[nt]:
                        conflit_regle = table[nt][production[0].name]
                        if conflit_regle[0].name == '^':  # Règle vide déjà présente
                            # Remplacez la règle vide par la nouvelle règle
                            table[nt][production[0].name] = production
                        else:
                            conflits.append((nt, production[0].name, table[nt][production[0].name], production))
                    else:
                        table[nt][production[0].name] = production
                
                elif production[0].type_token == "non_terminal":
                    for terminal in self.grammaire.premiers[production[0].name]:
                        if terminal in table[nt]:
                            conflit_regle = table[nt][terminal]
                            if conflit_regle[0].name == '^':  # Règle vide déjà présente
                                # Remplacez la règle vide par la nouvelle règle
                                table[nt][terminal] = production
                            else:
                                conflits.append((nt, terminal, table[nt][terminal], production))
                        else:
                            table[nt][terminal] = production
        
        if conflits:
            print("Conflits détectés dans la table d'analyse (les règles vides ont été traitées) :")
            for nt, terminal, prod1, prod2 in conflits:
                print(f"Conflit pour {nt} avec le terminal {terminal}:")
                print(f"  Production 1: {[token.name for token in prod1]}")
                print(f"  Production 2: {[token.name for token in prod2]}")
                
        return table



if __name__ == '__main__':
    grammaire_test = Grammaire('docs/Grammaire_PCL.txt')
    print(grammaire_test)
    print("#######################")
    print(f"Les premiers de la grammaire : {grammaire_test.premiers}\nLes suivants de la grammaire : {grammaire_test.suivants}")
    print("#######################")

    table_analyse = TableAnalyse(grammaire_test)





