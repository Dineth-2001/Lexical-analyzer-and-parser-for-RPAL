class AST:
    def __init__(self, root):
        self.root = root

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        if isinstance(node, tuple):
            print("  " * level + str(node[0]))
            for child in node[1:]:
                self.print_tree(child, level + 1)
        else:
            print("  " * level + str(node))
