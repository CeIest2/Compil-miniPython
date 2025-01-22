import re
import os
from colorama import init, Fore, Style

class Liste_token:

    def __init__(self):
        self.liste_token    = []
        self.dico_idf       = {}
        self.nb_identifiant = 0
        self.dico_char      = {}
        self.nb_char        = 0
        self.dico_number    = {}
        self.nb_number      = 0 
        self.dict_lexique = {"<ERROR>" : -1,"+" : 1,"-" : 2,"*" : 3,"/" : 4,":" : 5,"%" : 6,"if" : 9,
                             "then" : 10,"<" : 12,">" : 13,
                             "(" : 14,")" : 15,"[" : 16,"]" : 17,"not" : 19,"def" : 20,"or" : 21,
                             "and" : 22,"<=" : 23,">=" : 24,
                             "==" : 25,"!=" : 26,"True" : 27,"False" : 28,"None" : 29,"//" : 30,
                             "," : 31,"for" : 32,"in" : 33,
                             "print" : 34,"return" : 35,"BEGIN" : 36,"END" : 37, "NEWLINE" : 38,
                             "EOF" : 39, "identifiant" : 40, "char" : 41, "number":42, "=": 43,
                             "else": 44}
        self.liste_messages_erreurs = []


    def add_token_in_liste(self,token, etat):

        #print(f" on add un token : {token}")
        
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
            self.message_erreur("Caractère non reconnue par le language", token)
            self.liste_token.append(-1)

        return None
    

    def reconstruire_texte(self):
        texte_reconstruit = ""
        indentation_level = 0  # Pour gérer le niveau d'indentation

        for token in self.liste_token:
            if isinstance(token, int):
                if token == 38:  # NEWLINE
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                elif token == 36:  # BEGIN 
                    indentation_level += 1
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                elif token == 37:  # END 
                    indentation_level = max(0, indentation_level - 1)
                    texte_reconstruit = texte_reconstruit.rstrip() + "\n" + "    " * indentation_level
                else:
                    texte_reconstruit += list(self.dict_lexique.keys())[list(self.dict_lexique.values()).index(token)] + " "
            
            elif isinstance(token, tuple):
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

    def reconstruction_last_line(self):
        if not self.liste_token:
            return ""
        
        index = len(self.liste_token) - 1

        if self.liste_token[index] == 38:
            index -= 1
            if index < 0:
                return ""
        
        ligne_tokens = []
        while index >= 0 and self.liste_token[index] != 38:
            ligne_tokens.insert(0, self.liste_token[index])  # Insère au début pour garder l'ordre
            index -= 1

        ligne_texte = ""
        for token in ligne_tokens:
            if isinstance(token, int):
                if token in self.dict_lexique.values():
                    ligne_texte += list(self.dict_lexique.keys())[list(self.dict_lexique.values()).index(token)] + " "
            
            elif isinstance(token, tuple):
                token_type, token_value = token
                if token_type == 40:  # Identifiant
                    for ident, id_value in self.dico_idf.items():
                        if id_value == token_value:
                            ligne_texte += ident + " "
                            break
                elif token_type == 41:  # Char
                    for char, char_value in self.dico_char.items():
                        if char_value == token_value:
                            ligne_texte += '"' + char + '" '
                            break
                elif token_type == 42:  # Nombre
                    for nombre, num_value in self.dico_number.items():
                        if num_value == token_value:
                            ligne_texte += nombre + " "
                            break
        
        return ligne_texte.strip()

    def est_dans_intervalle_int64(self,valeur):
        # Bornes d'un entier signé 64 bits
        INT64_MIN = -2**63
        INT64_MAX = 2**63 - 1

        # Vérifier si la valeur est dans l'intervalle
        return INT64_MIN <= valeur <= INT64_MAX
    
    def message_erreur(self, type_erreur, token_probleme, token_index=None):
        """
        Crée un message d'erreur formaté.
        
        Args:
            type_erreur (str): Le type d'erreur à afficher
            token_probleme (str): Le token qui cause l'erreur
            token_index (int, optional): L'index du token problématique dans la liste_token
        """
        if token_index is not None:
            # Reconstruction de la ligne spécifique contenant le token problématique
            ligne_numero = 1  # Compte les NEWLINE jusqu'à l'index
            ligne_courante = []
            index_dans_ligne = 0
            
            for i in range(token_index + 1):
                if self.liste_token[i] == 38:  # NEWLINE
                    ligne_numero += 1
                    ligne_courante = []
                    index_dans_ligne = 0
                else:
                    ligne_courante.append(self.liste_token[i])
                    index_dans_ligne += 1
            
            # Reconstruction du texte de la ligne jusqu'au token problématique
            ligne_texte = ""
            for token in ligne_courante[:index_dans_ligne]:
                if isinstance(token, int):
                    if token in self.dict_lexique.values():
                        ligne_texte += list(self.dict_lexique.keys())[list(self.dict_lexique.values()).index(token)] + " "
                elif isinstance(token, tuple):
                    token_type, token_value = token
                    if token_type == 40:  # Identifiant
                        for ident, id_value in self.dico_idf.items():
                            if id_value == token_value:
                                ligne_texte += ident + " "
                                break
                    elif token_type == 41:  # Char
                        for char, char_value in self.dico_char.items():
                            if char_value == token_value:
                                ligne_texte += '"' + char + '" '
                                break
                    elif token_type == 42:  # Nombre
                        for nombre, num_value in self.dico_number.items():
                            if num_value == token_value:
                                ligne_texte += nombre + " "
                                break
        else:
            # Comportement original
            ligne_texte = self.reconstruction_last_line()
            ligne_numero = self.liste_token.count(38) + 1

        # Création du message d'erreur formaté
        error_message = (
            f"{Fore.RED}File \"{os.path.abspath(__file__)}\", line {ligne_numero}{Style.RESET_ALL}\n"
            f"{ligne_texte.strip()}{Fore.RED}{token_probleme}{Style.RESET_ALL}\n"
            f"{' ' * len(ligne_texte.strip())}{Fore.GREEN}^^^{Style.RESET_ALL}"
            f"\n{Fore.YELLOW}{type_erreur}{Style.RESET_ALL}"
        )
        self.liste_messages_erreurs.append(error_message)

    def afficher_erreurs(self):
        for message in self.liste_messages_erreurs:
            print(message)



def analyseur(fichier : str) -> Liste_token:
    """
        On prend en entré le fichier à analyser 
        et on va retourner la liste des token et une erreur ( si il y a pas d erreur c'est None)
    """

    etat = "debut_ligne"

    liste_token = Liste_token()
    erreur = None
    indentation_courante = [0]

    liste_token.add_token_in_liste("NEWLINE", etat)

    with open(fichier, 'r') as fichier:
        caractere = fichier.read(1)  
        while True :  # en cas d'apparition d'une erreur, on stop l'analyse
            if not caractere:  # condition de fin de lecture
                break
            
            if etat == "debut_ligne":
                if caractere == "\n":
                    liste_token.add_token_in_liste("NEWLINE", etat)
                    caractere = fichier.read(1)
                    etat = "debut_ligne"
                    continue
                # On compte le nombre d'indentation
                indentation = 0
                if caractere == ' ':
                    indentation =  1
                    caractere = fichier.read(1)
                    while caractere == ' ':
                        indentation += 1
                        caractere = fichier.read(1)

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
                        liste_token.message_erreur(liste_token.message_erreur("Erreur d'indentation", caractere))

            if caractere == " ":
                caractere = fichier.read(1)
                continue

            if caractere == "#":
                # On passe dans l'état de lecteur d'un commentaire 
                etat = "commentaire"
                while caractere != "\n":
                    caractere = fichier.read(1)
                    continue
                if liste_token.liste_token[-1] != 38 and liste_token.liste_token[-1] != 36 and liste_token.liste_token[-1] != 37:
                    liste_token.add_token_in_liste("NEWLINE", etat)
                etat = "debut_ligne"
                caractere = fichier.read(1)
                continue
                


            if caractere in ("1","2","3","4","5","6","7","8","9","0"):
                # cas de lecteur d'un entier
                nombre = caractere
                etat = "nombre"
                caractere = fichier.read(1)
                while caractere in ("1","2","3","4","5","6","7","8","9","0"):
                    nombre += caractere
                    caractere = fichier.read(1)
                if liste_token.est_dans_intervalle_int64(int(nombre)):
                    liste_token.add_token_in_liste(nombre, etat)
                    etat = "in_line"
                    continue
                else:
                    liste_token.message_erreur("int overflow", nombre)


            if re.compile(r'[a-zA-Z_]').match(caractere):
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
                    liste_token.message_erreur("! n'est pas disponible en mini-python, != et not le sont", caractere)
                    liste_token.add_token_in_liste("<ERROR>", etat)
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
                if caractere == "/":
                    caractere = fichier.read(1)
                    if caractere == "/":
                        liste_token.add_token_in_liste("//", etat)
                        caractere = fichier.read(1)
                        continue
                    else:
                        liste_token.add_token_in_liste("/", etat)
                        print(caractere)
                        etat = "in_line"
                        continue
                liste_token.add_token_in_liste(caractere, etat)
                caractere = fichier.read(1)
                continue

    
            liste_token.message_erreur("Caractère non recoonnue par le language", caractere)
            liste_token.add_token_in_liste("<ERROR>", etat)
            try:
                caractere = fichier.read(1)
            except:
                # en cas de fin de fichier on peut soritr de la boucle
                break
    if liste_token.liste_token[-1] != 36:
        liste_token.add_token_in_liste("NEWLINE", etat)
    # il faut aussi dépile les dernières imdentations et rajouter le token d end of file
    while len(indentation_courante)>1:
        liste_token.add_token_in_liste("END", etat)
        indentation_courante.pop()
    liste_token.add_token_in_liste("EOF", etat)

    return liste_token


if __name__=='__main__':

    liste_token = analyseur("fichier_test/fichier_test_lexeur/mini_test.txt")
    print(liste_token.reconstruire_texte())
    print(f"liste des tokens : {liste_token.liste_token}")
    print(f"dico des chars : {liste_token.dico_char}")
    print(f"dico des identifiant : {liste_token.dico_idf}")
    print(f"ldico des num : {liste_token.dico_number}")


    if liste_token.liste_messages_erreurs == []: print("analyse du fichier a réussi")
    else : 
        print("analyse du fichier n'a pas pu aboutir")
        print("### Erreurs lexicals ###")
        for message in liste_token.liste_messages_erreurs:
            print("========================================")
            print(message)