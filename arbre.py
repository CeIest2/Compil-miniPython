from graphviz import Digraph

class ASTNode:
    def __init__(self, value):
        self.value = str(value)  # Convertir en chaîne
        self.children = []  # Liste ordonnée des fils
        self.nb_children = 0
        self.parent = None  # Référence vers le parent

    def add_child(self, child, index=None):
        """Ajouter un fils à un index spécifique ou à la fin"""
        if child is not None :
            if index is not None:
                self.children.insert(index, child)
                child.parent = self
            else:
                self.children.append(child)
                child.parent = self
            self.nb_children += 1


def const_test_arbre():
    root = ASTNode('root')
    child1 = ASTNode('child1')
    child2 = ASTNode('child2')
    child3 = ASTNode('child3')
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    root.children[1].add_child(ASTNode('child4'))
    return root


def visualize_ast(root):
    dot = Digraph()
    int_to_token = {
        1: "+", 2: "-", 3: "*", 4: "/", 5: ":", 6: "%", 9: "if", 10: "then",
        12: "<", 13: ">", 14: "(", 15: ")", 16: "[", 17: "]", 19: "not",
        20: "def", 21: "or", 22: "and", 23: "<=", 24: ">=", 25: "==",
        26: "!=", 27: "True", 28: "False", 29: "None", 30: "//",
        31: ",", 32: "for", 33: "in", 34: "print", 35: "return",
        36: "BEGIN", 37: "END", 38: "NEWLINE", 39: "EOF",
        40: "identifiant", 41: "char", 42: "number", 43: "=", 44: "else"
    }

    
    def add_nodes_edges(node, parent=None):
        if node is None:
            return
        
        # Traduire la valeur pour l'affichage si elle est un entier
        try:
            display_value = int_to_token.get(int(node.value), str(node.value))
        except ValueError:
            display_value = node.value
        # Ajouter le nœud actuel
        dot.node(str(id(node)), display_value)
        
        # Si le nœud a un parent, ajouter une arête
        if parent is not None:
            dot.edge(str(id(parent)), str(id(node)))
        
        # Ajouter les enfants récursivement
        for child in node.children:
            add_nodes_edges(child, node)
    
    # Construire le graphe
    add_nodes_edges(root)
    dot.render('arbre_syntaxique', format='png', cleanup=True)  # Générer le fichier PNG
    dot.view()  # Ouvrir l'image générée

if __name__ == '__main__':
    # Utilisation
    root = const_test_arbre()
    visualize_ast(root)