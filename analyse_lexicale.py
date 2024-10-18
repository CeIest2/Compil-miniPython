

def analyse_lexicale (mini_py) : 
# mini_py une chaine de caractères

    dict_lexique = {
        "+" : 1,
        "-" : 2,
        "*" : 3,
        "/" : 4,
        ":" : 5,
        "%" : 6,
        "if" : 9,
        "then" : 10,
        "else" : 11,
        "<" : 12,
        ">" : 13,
        "(" : 14,
        ")" : 15,
        "[" : 16,
        "]" : 17,
        "not" : 19,
        "def" : 20,
        "or" : 21,
        "and" : 22,
        "<=" : 23,
        ">=" : 24,
        "==" : 25,
        "!=" : 26,
        "True" : 27,
        "False" : 28,
        "None" : 29,
        "//" : 30,
        "," : 31,
        "for" : 32,
        "in" : 33,
        "print" : 34,
        "return" : 35,
        "BEGIN" : 36,
        "END" : 37,
        "NEWLINE" : 38,
        "EOF" : 39,
        "def" : 40
    }

    dict_idf = { }
    dict_char = { }

    lexique = []

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    digits = ['0','1','2','3','4','5','6','7','8','9']

    i = 0

    while i < len(mini_py):

        # mots cles ou idf
        if mini_py[i] in alphabet :
            x=mini_py[i]
            i+=1
            while mini_py[i] in alphabet or mini_py[i] in digits or mini_py[i] == "_": 
                x+=mini_py[i]
                i+=1
            if x in dict_lexique.keys():
                lexique.append(dict_lexique[x])     # ajout du token du mot cle
            else :
                if dict_idf == {} :
                    dict_idf[x] = 1
                elif x not in dict_idf.keys():
                    dict_idf[x] = max(dict_idf.values())+1
                lexique.append((7,dict_idf[x]))     # ajout du token idf

        # espaces -> FAUX
        elif mini_py[i] == " ":
            i+=1    # gerer tab 

        # integers
        elif mini_py[i] in digits :
            x = mini_py[i]
            i+=1
            while mini_py[i] in digits :
                x += mini_py[i]
                i+=1
            lexique.append((8,int(x)))                    # ajout du token cst

        # char
        elif mini_py[i] == '"' :
            x = mini_py[i]
            i+=1
            while mini_py[i] != '"' :
                if mini_py[i] == "\\": # dans str écrire \" ou " ?
                    x += mini_py[i]
                    i+=1
                x += mini_py[i]
                i+=1
            x = mini_py[i] # il faut gérer erreur si pas de guillement fermante
            i+=1
            if dict_char == {} :
                dict_char[x] = 1
            elif x not in dict_char.keys():
                dict_char[x] = max(dict_char.values())+1
            lexique.append((18,dict_char[x]))     # ajout du token char



