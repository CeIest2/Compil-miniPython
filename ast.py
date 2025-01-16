def simplify_rules(value,parse_tree):
    
    if value == "file":
        return ASTNode("file", [
            simplify_tree(child) for child in parse_tree.children
            if child.value not in [38, 39] ]) # NEWLINE EOF

    if value == "start_func":
        return ASTNode("functions", [
            simplify_tree(child) for child in parse_tree.children if child.value == "def"])

    if value == "def":
        name = parse_tree.children[1].value  # Nom de la fonction (40 : identifiant)
        params = simplify_parameters(parse_tree.children[4])  # Paramètres
        body = simplify_tree(parse_tree.children[-1])  # Corps (suite)
        return ASTNode("def", [ASTNode(name), params, body])

    if value == "parameters":
        if not parse_tree or parse_tree.value == "^":
            return ASTNode("parameters", [])
        params = [simplify_tree(child) for child in parse_tree.children if child.value == 40]
        return ASTNode("parameters", params)

    if value == "start_stmt":
        return ASTNode("statements", [
            simplify_tree(child) for child in parse_tree.children if child.value == "stmt"])

    if value == "stmt":
        if parse_tree.children[0].value == "if":
            condition = simplify_tree(parse_tree.children[1])  # Condition
            then_branch = simplify_tree(parse_tree.children[-2])  # Then
            else_branch = simplify_tree(parse_tree.children[-1]) if len(parse_tree.children) > 4 else None  # Else
            return ASTNode("if", [condition, then_branch, else_branch])
        else:
            return simplify_tree(parse_tree.children[0])  # Simple statement


    # if value == "if":
    #     condition = simplify_tree(parse_tree.children[1])  # Condition
    #     then_branch = simplify_tree(parse_tree.children[-2])  # Bloc "then"
    #     else_branch = simplify_tree(parse_tree.children[-1]) if len(parse_tree.children) > 4 else None  # Bloc "else"
    #     return ASTNode("if", [condition, then_branch, else_branch])


    if value == "expr":
        left = simplify_tree(parse_tree.children[0])  # Gauche
        if len(parse_tree.children) > 1:  # Si opérateur binaire
            operator = parse_tree.children[1].value
            right = simplify_tree(parse_tree.children[2])
            return ASTNode(operator, [left, right])
        return left  # Expression simple

    if value == "const":
        return ASTNode("const", [ASTNode(parse_tree.children[0].value)])

    if value == "simple_stmt":
        if parse_tree.children[0].value == 35:  # RETURN
            expr = simplify_tree(parse_tree.children[1])
            return ASTNode("return", [expr])
        else:
            return simplify_tree(parse_tree.children[0])  # D'autres cas

    if value == "binop":
        return ASTNode(parse_tree.children[0].value)  # Opérateur









def simplify_tree(parse_tree):
    """
    Simplifie un arbre de dérivation en AST.
    - parse_tree: L'arbre de dérivation d'entrée.
    Retourne : un nœud AST simplifié.
    """

    if not parse_tree.children:
        if parse_tree.value in [38,36,37,31,14,15]:  # NEWLINE, BEGIN, END, ","", (, ) inutiles
            return None
        return ASTNode(parse_tree.value)

    value = parse_tree.value
    
    return simplify_rules(value,parse_tree)

    # Parcourir et simplifier les enfants
    simplified_children = [simplify_tree(child) for child in parse_tree.children]
    simplified_children = [child for child in simplified_children if child]  # Supprimer None
    return ASTNode(value, simplified_children)

