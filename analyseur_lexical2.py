import re

class Liste_token:

    def __init__(self):
        self.liste_token    = []
        self.dico_idf       = {}
        self.nb_identifiant = 0
        self.dico_char      = {}
        self.nb_char        = 0
        self.dico_number    = {}
        self.nb_number      = 0 
        self.dict_lexique = {"+" : 1,"-" : 2,"*" : 3,"/" : 4,":" : 5,"%" : 6,"if" : 9,"then" : 10,"<" : 12,">" : 13,"(" : 14,")" : 15,"[" : 16,"]" : 17,"not" : 19,"def" : 20,"or" : 21,"and" : 22,"<=" : 23,">=" : 24,"==" : 25,"!=" : 26,"True" : 27,"False" : 28,"None" : 29,"//" : 30,"," : 31,"for" : 32,"in" : 33,"print" : 34,"return" : 35,"BEGIN" : 36,"END" : 37,"NEWLINE" : 38,"EOF" : 39, "identifiant" : 40, "char" : 41, "number":42, "=": 43}



    def add_token_in_liste(self,token, etat):

        print(f" on add un token : {token}")
        
        if token in self.dict_lexique.keys():
            self.liste_token.append(self.dict_lexique[token])

        elif etat == "nombre":
            if token in self.dico_number:
                self.liste_token.append((42,self.dico_number[token]))
            else:
                self.dico_number[token] = self.nb_number + 1
                self.nb_number += 1
                self.liste_token.append((42,self.dico_number[token]))
        
        elif etat == "identifiant":
            if token in self.dico_idf:
                self.liste_token.append((40,self.dico_idf[token]))
            else:
                self.dico_idf[token] = self.nb_identifiant + 1
                self.nb_identifiant += 1
                self.liste_token.append((40,self.dico_idf[token]))

        elif etat == "char":
            if token in self.dico_char:
                self.liste_token.append((41,self.dico_char[token]))
            else:
                self.dico_char[token] = self.nb_char + 1
                self.nb_char += 1
                self.liste_token.append((41,self.dico_char[token]))

        else:
            print(f" y a une merde quelque part là, token pa identifier : |{token}| etat : {etat}")
            return -1

        return None
    

    def reconstruire_texte(self):
        texte_reconstruit = ""
        indentation_level = 0  # Pour gérer le niveau d'indentation

        # Parcours de chaque token dans `self.liste_token`
        for token in self.liste_token:
            if isinstance(token, int):
                if token == 38:  # NEWLINE
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                elif token == 36:  # BEGIN (augmentation de l'indentation)
                    indentation_level += 1
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                elif token == 37:  # END (diminution de l'indentation)
                    indentation_level = max(0, indentation_level - 1)
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                else:
                    # Autres tokens de `dict_lexique`
                    texte_reconstruit += list(self.dict_lexique.keys())[list(self.dict_lexique.values()).index(token)] + " "
            
            elif isinstance(token, tuple):
                # Cas des tokens avec des valeurs associées (identifiants, chars, et nombres)
                token_type, token_value = token
                
                if token_type == 40:  # Identifiant
                    for ident, id_value in self.dico_idf.items():
                        if id_value == token_value:
                            texte_reconstruit += ident + " "
                            break
                
                elif token_type == 41:  # Char
                    for char, char_value in self.dico_char.items():
                        if char_value == token_value:
                            texte_reconstruit += '"' + char + '" '
                            break
                
                elif token_type == 42:  # Nombre
                    for nombre, num_value in self.dico_number.items():
                        if num_value == token_value:
                            texte_reconstruit += nombre + " "
                            break
            
            else:
                print(f"Token inconnu dans la liste : {token}")

        # Nettoyer les espaces en fin de ligne et les lignes vides finales
        texte_reconstruit = "\n".join(line.rstrip() for line in texte_reconstruit.strip().splitlines())

        return texte_reconstruit




def analyseur(fichier : str):
    """
        On prend en entré le fichier à analyser 
        et on va retourner la liste des token et une erreur ( si il y a pas d erreur c'est None)
    """

    etat = "debut_ligne"

    liste_token = Liste_token()
    dico_idf = {}
    dico_char = {}
    dico_number = {}
    erreur = None
    indentation_courante = [0]

    with open(fichier, 'r') as fichier:
        caractere = fichier.read(1)  
        while True :  # en cas d'apparition d'une erreur, on stop l'analyse
            if not caractere:  # condition de fin de lecture
                break
            
            if etat == "debut_ligne":
                # On compte le nombre d'indentation
                indentation = 0
                if caractere == ' ':
                    indentation =  1
                    caractere = fichier.read(1)
                    while caractere == ' ':
                        indentation += 1
                        caractere = fichier.read(1)
                        continue
                    if caractere == "\n":
                        caractere = fichier.read(1)
                        etat = "debut_ligne"
                        continue

                # ici on va faire toute la gestion des indentations au début des lignes
                if indentation == indentation_courante[-1] : pass
                elif indentation > indentation_courante[-1]: 
                    indentation_courante.append(indentation)
                    liste_token.add_token_in_liste("BEGIN",etat)
                elif indentation < indentation_courante[-1]:
                    while indentation_courante and indentation_courante[-1] > indentation:
                        liste_token.add_token_in_liste("END", etat)
                        indentation_courante.pop()

                    # Si la pile est vide ou que l'indentation courante n'a pas atteint le niveau attendu
                    if not indentation_courante or indentation_courante[-1] != indentation:
                        erreur = "erreur avec les indentations"
                        print("erreur dindentation ici")
                        print(liste_token.reconstruire_texte())
                        return erreur

            if caractere == " ":
                caractere = fichier.read(1)
                continue

            if caractere == "#":
                # On passe dans l'état de lecteur d'un commentaire 
                etat = "commentaire"
                while caractere != "\n":
                    caractere = fichier.read(1)
                    continue
                liste_token.add_token_in_liste("NEWLINE", etat)
                etat = "debut_ligne"
                caractere = fichier.read(1)
                continue
                


            if caractere in ("1","2","3","4","5","6","7","8","9","0"):
                # cas de lecteur d'un entier
                if etat == "debut_ligne":
                    return " on ne peut pas avoir de int au bébut d une ligne"
                nombre = caractere
                etat = "nombre"
                caractere = fichier.read(1)
                while caractere in ("1","2","3","4","5","6","7","8","9","0"):
                    nombre += caractere
                    caractere = fichier.read(1)
                liste_token.add_token_in_liste(nombre, etat)
                etat = "in_line"
                continue
            

            if re.compile(r'[a-zA-Z_]').match(caractere):
                print("oui")
                etat = "identifiant"
                identifiant_courant = caractere
                caractere = fichier.read(1)
                while re.compile(r'[a-zA-Z0-9_]').match(caractere):
                    identifiant_courant += caractere
                    caractere = fichier.read(1)
                liste_token.add_token_in_liste(identifiant_courant, etat)
                etat = "in_line"
                continue
            
            if caractere == '"':
                # On est alors dans le cas d'une lecture d'un char
                etat = "char"
                char_courant = ""
                caractere = fichier.read(1)
                fin_char = False
                cara_echappement = False
                
                while fin_char == False:
                    if caractere != '"' and not cara_echappement:
                        if caractere !=  """\\""": char_courant += caractere
                        else: cara_echappement = True
                        caractere = fichier.read(1)
                        continue
                    if cara_echappement:
                        char_courant += caractere
                        cara_echappement = False
                        caractere = fichier.read(1)
                        continue
                    if caractere == '"':
                        fin_char = True
                liste_token.add_token_in_liste(char_courant, etat)
                etat = "in_line"
                caractere = fichier.read(1)
                continue

            if caractere in ["<",">","="]:
                etat = "comparaison"
                expression = caractere
                caractere = fichier.read(1)
                if caractere == "=":
                    expression += caractere
                    liste_token.add_token_in_liste(expression,etat)
                    caractere = fichier.read(1)
                    continue
                else:
                    liste_token.add_token_in_liste(expression, etat)
                    etat = 'in_line'
                    continue
            if caractere == "!":
                expression = caractere
                caractere = fichier.read(1)
                if caractere != "=":
                    return "erreur, il faut un = normalement ici"
                else:
                    expression += caractere
                    liste_token.add_token_in_liste(expression, etat)
                    caractere = fichier.read(1)
                    continue
            

            if caractere == '\n':
                caractere = fichier.read(1)
                liste_token.add_token_in_liste("NEWLINE", etat)
                etat = "debut_ligne"
                continue

            if caractere in liste_token.dict_lexique:
                etat = "cara_unique"
                liste_token.add_token_in_liste(caractere, etat)
                caractere = fichier.read(1)
                continue

            print(liste_token.liste_token)
            print(f"y a erreur la normalement {caractere}")
            return -1


            




                        



    print(liste_token.reconstruire_texte())
    print(liste_token.liste_token)
    print("finit")


analyseur("test_2.txt")