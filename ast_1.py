from arbre import Arbre


def simplify_rules(parse_tree):

    value = parse_tree.value
    
    if value == "<file>":
        ast = Arbre("<file>")
        for child in parse_tree.children :
            if child.value not in ["38", "39"]: # NEWLINE EOF
                ast.add_child(simplify_tree(child))
        return ast

    elif value == "<start_func>":
        ast = Arbre("<FUNCTION>")
        for child in parse_tree.children:
            if child.value == "<def>":
                return (simplify_tree(child))
        return ast

    elif value == "<def>":
        for child in parse_tree.children :
            if child.value == "40":
                # Nom de la fonction (40 : identifiant)
                name = Arbre(child.num_identifiant)
            elif child.value == "<first_para>":
                child.value ='<parameters>'
                params = simplify_tree (child)
            elif child.value == "<suite>":
                body = simplify_tree(child)  # Corps (suite)
        ast = Arbre("<function>")
        ast.add_child(name)
        ast.add_child(params)
        ast.add_child(body)
        return ast
    
    elif value == "<suite>":
        ast = Arbre("<body>")
        for child in parse_tree.children:
            # print ('body ; ', child.value)
            if child.value != '<start_stmt>':
                ast.add_child(simplify_tree(child))
            else :
                if parse_tree.children[0].value == '^':
                    return None
                else:
                    L=simplify_statements(parse_tree,[])
                    L.reverse()
                    for child in L:
                        ast.add_child(child)
                    return ast 
        return ast
    
    elif value =="<parameters>":
        ast = Arbre("<parameters>")
        L=simplify_parameters(parse_tree,[])
        L.reverse()
        for child in L :
            ast.add_child(child)
        return ast

    # elif value == "<start_stmt>":
    #     if parse_tree.children[0].value == '^':
    #         return None
    #     else:
    #         ast= Arbre("<statements>")
    #         L=simplify_statements(parse_tree,[])
    #         L.reverse()
    #         for child in L:
    #             ast.add_child(child)
    #         return ast    

    elif value == "<stmt>":
        for child in parse_tree.children:
            #print('child_stmt : ',child.value)

            if child.value == "9":               # if
                condition = simplify_tree(parse_tree.children[2])  # Condition
                if_body = simplify_tree(parse_tree.children[1])  # Then
                else_branch = simplify_tree(parse_tree.children[0]) if len(parse_tree.children) > 4 else None  # Else
                ast= Arbre(child.value)
                ast.add_child(condition)
                ast.add_child(if_body)
                ast.add_child(else_branch)
                return ast
            
            elif child.value == "<simple_stmt>":
                return simplify_tree(child)
            
            elif child.value == "32":                         #for
                condition = Arbre("33")
                idf = parse_tree.children[3]
                condition.add_child(Arbre(idf.num_identifiant))
                condition.add_child(simplify_tree(parse_tree.children[1]))
                body = simplify_tree(parse_tree.children[0])
                ast = Arbre("32")
                ast.add_child(condition)
                ast.add_child(body)
                return ast
            # pas de while ??
        return None
    
    elif value == "<suite_if>":
        for child in parse_tree.children:
            #print('suit if : ',child.value)
            if child.value == "^":
                return None
            elif child.value == "44":
                suite_if = Arbre("44")
            elif child.value == "<suite>":
                suite = simplify_tree(child)
        suite_if.add_child(suite)
        return suite_if

    elif value == "<expr>":
        # for child in parse_tree.children:
        #     print (child.value)
        if parse_tree.children[1].value=='<const>':
            const = parse_tree.children[1].children[0]
            if const.value =="42":
                left = Arbre("int : "+str(const.num_identifiant))  # Gauche
            elif const.value =="41":
                left = Arbre("str : "+const.num_identifiant)
            else :
                left = Arbre(const.value)
            if parse_tree.children[0].children[0].value == '^':  
                return left
            else :
                right = simplify_tree(parse_tree.children[0])
                search_op = right
                # while len(search_op.children) in [0,2]:
                # if search_op.children == []
                #     search_op
                # if len(search_op.children) == 1:
                #     search_op.add_child(left)
                ast= Arbre(right.value)
                ast.add_child(left)
                for child in right.children:
                    ast.add_child(child)
                return ast
            
        elif parse_tree.children[1].value=='40':
            child=parse_tree.children[1]
            left = Arbre(child.num_identifiant)  # Gauche
            if parse_tree.children[0].children[0].value == '^':  
                return left
            else :
                right = simplify_tree(parse_tree.children[0])
                ast= Arbre(right.value)
                ast.add_child(left)
                for child in right.children:
                    ast.add_child(child)
                return ast
            
        elif parse_tree.children[-1].value=='17':
            expr2 = simplify_tree(parse_tree.children[0])       #right
            #depth = simplify_tree(parse_tree.children[1])       # ??
            expr = simplify_tree(parse_tree.children[2])        #left
            if expr2 == None:  
                return expr
            else :
                ast= Arbre(expr2.value)
                ast.add_child(expr)
                for child in expr2.children:
                    ast.add_child(child)
                return ast
            
        
        elif parse_tree.children[-1].value=='15':
            expr2 = simplify_tree(parse_tree.children[0])       #right
            expr = simplify_tree(parse_tree.children[1])        #left
            if expr2 == None:  
                return expr
            else :
                ast= Arbre(expr2.value)
                ast.add_child(expr)
                for child in expr2.children:
                    ast.add_child(child)
                return ast
            
        elif parse_tree.children[-1].value=='19':               #not
            expr2 = simplify_tree(parse_tree.children[0])       #right
            expr = simplify_tree(parse_tree.children[1])        #left
            expr_not = Arbre("19")
            expr_not.add_child(expr)
            if expr2 == None:  
                return expr_not
            else :
                ast= Arbre(expr2.value)
                ast.add_child(expr_not)
                for child in expr2.children:
                    ast.add_child(child)
                return ast


        #autres possibilités de <expr>
        return None  # Expression simple
    
    elif value == "<expr2>":
        # for child in parse_tree.children :
        #     print (child.value)
        if parse_tree.children[0].value == '^':
            return None
        
        elif parse_tree.children[2] and parse_tree.children[2].value=='<binop>':
            for child in parse_tree.children:
                print ('expr2 : ',child.value)
            binop = simplify_tree(parse_tree.children[2])
            expr = simplify_tree(parse_tree.children[1])
            # if expr.value not in ["21","22""19","12","13","23","24","25","26","1","2","3","4","6"]:
            binop.add_child(expr)
            return binop
            #gerer prio
            # ast = manage_prio_op(binop,expr)
            # ast.add_child(simplify_tree(parse_tree.children[0]))
            # return ast
        
        #autre possibilité


    elif value == "<const>":
        const = parse_tree.children[1].children[0]
        if const.value =="42":
            ast = Arbre("int : "+str(const.num_identifiant))
        elif const.value =="41":
            ast = Arbre("str : "+const.num_identifiant)
        else :
            ast = Arbre(const.value)
        return ast

    elif value == "<depth>":
        return simplify_depth(parse_tree)
    
    # if value == "<suite_ident_simple_stmt>":

    if value == "<suite_expr>":
        if parse_tree.children[0]=="^":
            return None
        else :
            for child in parse_tree.children:
                print ("suite_expr : ", child.value)
                ###commment ca marche ???


    elif value == "<simple_stmt>":
        # print (parse_tree.children[0].value,",",parse_tree.children[1].value)

        if parse_tree.children[1] and parse_tree.children[1].value == "35":  # RETURN
            expr = simplify_tree(parse_tree.children[0])
            ast= Arbre("35")
            ast.add_child(expr)
            return ast
        
        elif parse_tree.children[0].value == "<suite_ident_simple_stmt>":
            if parse_tree.children[1].value == "40" and len(parse_tree.children) > 1: #cas d'une affectation
                affect_suite = parse_tree.children[0] #Le noeud contenant la suite de l'affectation
                #print (affect_suite.children[0].value,',',affect_suite.children[1].value)
                if affect_suite.children[1] and affect_suite.children[1].value == "43":
                    #print("la ",affect_suite.children[0].value)
                    expression = simplify_tree(affect_suite.children[0])  # Simplifie l'expression d'affectation
                    ast = Arbre("43")
                    ast.add_child(Arbre(parse_tree.children[1].num_identifiant))  # Ajouter le nom de la variable
                    ast.add_child(expression)  # Ajouter l'expression assignée
                    return ast
                elif affect_suite.children[0] == '<suite_ident_expr>':
                    return simplify_tree(affect_suite.children[0])
        
        # pas vérifié
        elif parse_tree.children[0].value == "19": #cas d'un Not suivi d'expression
            
            expression = simplify_tree(parse_tree.children[1])
            ast = Arbre("19")
            ast.add_child(expression) #ajoutg de la première expression

            if len(parse_tree.children) > 2: #traitement de <expr2> si nécessaire
                expr2 = simplify_tree(parse_tree.children[2])
                ast.add_child(expr2)
            
            if len(parse_tree.children ) > 3: #traitement de <suite_expr> si nécessaire
                suite_expr = simplify_tree(parse_tree.children[3]) 
                ast.add_child(suite_expr)
            
            return ast
        
        elif parse_tree.children[1] and parse_tree.children[1].value == '34': # cas du print on ignore les parenthèses
            ast = Arbre("34")
            ast.add_child(simplify_tree(parse_tree.children[0]))
            return ast
        
        # elif parse_tree.children[-1] == "17" : # cas []

            
        else:#a check
            return simplify_tree(parse_tree.children[0])  # D'autres cas

    elif value == "<binop>":
        return Arbre(parse_tree.children[0].value)  # Opérateur
    
    elif value == "<suite_ident_expr>":
        if len(parse_tree.children)==1:
            return simplify_tree(parse_tree.children[0])
        else :
            for child in parse_tree.children :
                print("suite_ident_expr : ", child.value)
                #comment on fait ???

    return None



def simplify_parameters(param_node,L):
    """
    Simplifie une liste de paramètres.
    - param_node: nœud de paramètres dans l'arbre de dérivation.
    """
    if not param_node or param_node.value == "^":
        return L
    for child in param_node.children :
        if child.value == "40":
            ast=Arbre(child.num_identifiant)
            L.append(ast)
        elif child.value == "<parameters>":
            nested_params = simplify_parameters(child,L)
            L=L+nested_params
    return L


def simplify_statements(param_node,L):
    if not param_node or param_node.value == "^":
        return L
    for child in param_node.children :
        if child.value not in ["<start_stmt>","<start_stmt_2>","^"]:
            ast = simplify_tree(child)
            L.append(ast)
        else :
            nested_params = simplify_statements(child,L)
            L=L+nested_params
    return L


# def manage_prio_op(node1,node2):
#     op1 = node1.value
#     op2 = node2.value
#     dict_op = {
#     ("21",): 1,
#     ("22",): 2,
#     ("19",): 3,
#     ("12", "13", "23", "24", "25", "26"): 4,
#     ("1", "2"): 5,
#     ("3", "4", "6"): 6
# }
#     for key in dict_op.keys():
#         if op1 in key:
#             op1_prio = dict_op[key]
#         if op2 in key:
#             op2_prio = dict_op[key]
    
#     if op1_prio < op2_prio:
#         node1.add_child(node2)
#         return node1
#     else :
#         node = Arbre(op2)
#         node1.add_child(node2.children[0])
#         node.add_child(node1)
#         node.add_child(node2.children[1])
#     return node




def simplify_tree(parse_tree):
    """
    Simplifie un arbre de dérivation en AST.
    - parse_tree: L'arbre de dérivation d'entrée.
    Retourne : un nœud AST simplifié.
    """
    if not parse_tree:
        return None
    
    if parse_tree.value in ["38","36","37","31","14","15"]:  # NEWLINE, BEGIN, END, ","", (, ) inutiles
        return None
    
    if not parse_tree.children:
        return Arbre(parse_tree.value)
    
    value = parse_tree.value

    # Appliquer les règles de simplification
    simplified_node = simplify_rules(parse_tree)

    # Si aucune règle spécifique n'a été appliquée, simplifier récursivement
    # if not simplified_node:
    #     simplified_node = Arbre(parse_tree.value)
    #     for child in parse_tree.children:
    #         simplified_child = simplify_tree(child)
    #         if simplified_child:  # Vérifie que le nœud enfant n'est pas None
    #             simplified_node.add_child(simplified_child)

    return simplified_node


def simplify_depth(parse_tree):

    expressions = []

    #On traite la première expression après la virgule
    current_expr = parse_tree.children[1]
    expressions.append(simplify_tree(current_expr))

    #on traite les expressions qui suivent

    current_depth = parse_tree.children[2]
    while current_depth.value == "<depth>":
        expressions.append(simplify_tree(current_depth.children[1]))
        current_depth = current_depth.children[2]

    #on construit le noeud après avoir recup toute les expresssiosn dans expressions
    depth_node = Arbre("List")
    for i in  expressions:
        depth_node.add_child(i)
    
    return depth_node