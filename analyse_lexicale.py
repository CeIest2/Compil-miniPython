

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
        "#" : 20,
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

    i = 0

    while i < len(mini_py):
        if mini_py[i].isalpha() : # vérifier si is alpha ne prend pas les accents etc en compte
            x=mini_py[i]
            i+=1
            while mini_py[i].isalpha() or mini_py[i].isdigit() or mini_py[i] == "_": 
                x+=mini_py[i]
                i+=1
        


