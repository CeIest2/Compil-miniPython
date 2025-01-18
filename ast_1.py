from arbre import ASTNode


def simplify_rules(parse_tree):

    value = parse_tree.value
    
    if value == "<file>":
        ast = ASTNode("<file>")
        for child in parse_tree.children :
            if child.value not in [38, 39]: # NEWLINE EOF
                ast.add_child(simplify_tree(child))
        return ast

    if value == "<start_func>":
        ast = ASTNode("<function>")
        for child in parse_tree.children:
            if child.value == "<def>":
                ast.add_child(simplify_tree(child))
        return ast

    if value == "<def>":
        name = parse_tree.children[1].value  # Nom de la fonction (40 : identifiant)
        params = simplify_parameters(parse_tree.children[4])  # Paramètres
        body = simplify_tree(parse_tree.children[-1])  # Corps (suite)
        ast = ASTNode("<def>")
        ast.add_child(ASTNode(name))
        ast.add_child(params)
        ast.add_child(body)
        return ast

    if value == "<parameters>":
        return simplify_parameters(parse_tree)

    if value == "<start_stmt>":
        ast= ASTNode("<statements>")
        for child in parse_tree.children:
            if child.value == "<stmt>":
                ast.add_child(simplify_tree(child))
        return ast    

    if value == "<stmt>":
        if parse_tree.children[0].value == 9:               # if
            condition = simplify_tree(parse_tree.children[1])  # Condition
            if_body = simplify_tree(parse_tree.children[-2])  # Then
            else_branch = simplify_tree(parse_tree.children[-1]) if len(parse_tree.children) > 4 else None  # Else
            ast= ASTNode(9)
            ast.add_child(condition)
            ast.add_child(if_body)
            ast.add_child(else_branch)
            return ast
        else:
            return simplify_tree(parse_tree.children[0])  # Simple statement

    if value == "<expr>":
        left = simplify_tree(parse_tree.children[0])  # Gauche
        if len(parse_tree.children) > 1:  # Si opérateur binaire
            operator = parse_tree.children[1].value
            right = simplify_tree(parse_tree.children[2])
            ast= ASTNode(operator)
            ast.add_child(left)
            ast.add_child(right)
            return ast
        return left  # Expression simple

    if value == "<const>":
        ast= ASTNode("<const>")
        ast.add_child(ASTNode(parse_tree.children[0].value))

    if value == "<simple_stmt>":
        if parse_tree.children[0].value == 35:  # RETURN
            expr = simplify_tree(parse_tree.children[1])
            ast= ASTNode(35)
            ast.add_child(expr)
            return ast
        
        elif parse_tree.children[0].value == 40 and len(parse_tree.children) > 1: #cas d'une affectation
            if parse_tree.children[1].value == "<suite_ident_simple_stmt>":
                identifier = parse_tree.children[0]  # Le nœud contenant l'identifiant
                affect_suite = parse_tree.children[1] #Le noeud contenant la suite de l'affectation
                if affect_suite.children and affect_suite.children[0].value == 43:
                    expression = simplify_tree(affect_suite.children[1])  # Simplifie l'expression d'affectation
                    ast = ASTNode("Assignment")
                    ast.add_child(ASTNode("Identifier", identifier.value))  # Ajouter le nom de la variable
                    ast.add_child(expression)  # Ajouter l'expression assignée
                    return ast
        
        elif parse_tree.children[0].value == 19: #cas d'un Not suivi d'expression
            
            expression = simplify_tree(parse_tree.children[1])
            ast = ASTNode("Not")
            ast.add_child(expression) #ajoutg de la première expression

            if len(parse_tree.children) > 2: #traitement de <expr2> si nécessaire
                expr2 = simplify_tree(parse_tree.children[2])
                ast.add_child(expr2)
            
            if len(parse_tree.children ) > 3:

                suite_expr = simplify_tree(parse_tree.children[3])
                ast.add_child(suite_expr)
            
            return ast
        
        else:
            return simplify_tree(parse_tree.children[0])  # D'autres cas

    if value == "<binop>":
        return ASTNode(parse_tree.children[0].value)  # Opérateur

    return None



def simplify_parameters(param_node):
    """
    Simplifie une liste de paramètres.
    - param_node: nœud de paramètres dans l'arbre de dérivation.
    """
    if not param_node or param_node.value == "^":
        return ASTNode("<parameters>")
    ast = ASTNode("<parameters>")
    for child in param_node.children :
        if child.value ==40:
            ast.add_child(simplify_tree(child))
    return ast









def simplify_tree(parse_tree):
    """
    Simplifie un arbre de dérivation en AST.
    - parse_tree: L'arbre de dérivation d'entrée.
    Retourne : un nœud AST simplifié.
    """
    if not parse_tree:
        return None
    
    if parse_tree.value in [38,36,37,31,14,15]:  # NEWLINE, BEGIN, END, ","", (, ) inutiles
        return None
    
    if not parse_tree.children:
        return ASTNode(parse_tree.value)
    
    value = parse_tree.value

    # Appliquer les règles de simplification
    simplified_node = simplify_rules(parse_tree)

    # Si aucune règle spécifique n'a été appliquée, simplifier récursivement
    if not simplified_node:
        simplified_node = ASTNode(parse_tree.value)
        for child in parse_tree.children:
            simplified_child = simplify_tree(child)
            if simplified_child:  # Vérifie que le nœud enfant n'est pas None
                simplified_node.add_child(simplified_child)

    return simplified_node

