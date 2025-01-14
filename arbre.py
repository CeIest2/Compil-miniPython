from graphviz import Digraph

class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []  # Liste ordonnée des fils
        self.nb_children = 0
        self.parent = None  # Référence vers le parent

    def add_child(self, child, index=None):
        """Ajouter un fils à un index spécifique ou à la fin"""
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
    dot = Digraph(comment='AST')
    
    def add_nodes_edges(node, parent=None):
        dot.node(str(id(node)), node.value)
        if parent:
            dot.edge(str(id(parent)), str(id(node)))
        
        # Parcourir les enfants dans l'ordre
        for child in node.children:
            add_nodes_edges(child, node)
    add_nodes_edges(root)
    # Render to a file
    dot.render('ast_tree', view=True, format='png')


if __name__ == '__main__':
    # Utilisation
    root = const_test_arbre()
    visualize_ast(root)