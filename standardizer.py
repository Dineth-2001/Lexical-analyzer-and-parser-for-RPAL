from parser import Parser, Node
from scanner import Scanner

# The standardize function takes a file name as input and returns a standardized tree.
def standardize(file_name):
    # Tokenize the input file
    scanner = Scanner()
    with open(file_name, 'r') as file:
        code = file.read()
    tokens = scanner.tokenize(code)
    tokens.reverse()  

    # Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()

    # Standardize the AST
    st = make_standardized_tree(ast)
    return st

# The make_standardized_tree function takes a root node as input and returns a standardized tree.
def make_standardized_tree(root):
    # Recursively standardize the children
    if root.left:
        root.left = make_standardized_tree(root.left)
    if root.right:
        root.right = make_standardized_tree(root.right)

    # Apply standardization rules
    if root.label == "let" and root.left.label == "=":
        '''
                 let                gamma
                /   \               /    \    
               =     E   =>       lambda  E               
              / \                /     \
             X   E              X       E
        '''
        root.label = "gamma"
        lambda_node = Node("lambda")
        lambda_node.left = root.left.left
        lambda_node.right = root.left.right
        root.left = lambda_node

    elif root.label == "where" and root.right.label == "=":
        '''
                 where                gamma 
                 /   \                /    \
                E     =     =>      lambda  E
                     / \             /  \
                    X   E           X    E
        '''
        root.label = "gamma"
        lambda_node = Node("lambda")
        lambda_node.left = root.right.left
        lambda_node.right = root.right.right
        root.right = root.left
        root.left = lambda_node

    elif root.label == "function_form":
        '''
                 function_form                  =
                 /   |    \                    / \
                P    V+    E     =>           P   lambda
                                                   /   \
                                                  V    E                  
        '''
        root.label = "="
        lambda_node = Node("lambda")
        lambda_node.left = root.left.right
        lambda_node.right = root.right
        root.right = lambda_node

    elif root.label == "within" and root.left.label == "=" and root.right.label == "=":
        '''
                    within                =
                    /    \               / \
                   =      =     =>      X2   gamma
                  / \    / \                 /   \
                 X1  E1  X2 E2            lambda  E1 
                                          /    \
                                         X1    E2    
        '''
        root.label = "="
        gamma_node = Node("gamma")
        lambda_node = Node("lambda")
        lambda_node.left = root.left.left
        lambda_node.right = root.right.right
        gamma_node.left = lambda_node
        gamma_node.right = root.left.right
        root.left = root.right.left
        root.right = gamma_node

    elif root.label == "@":
        '''
                    @                gamma
                  / | \              /   \
                E1  N  E2    =>    gamma  E2
                                   /   \
                                  N     E1
        '''
        root.label = "gamma"
        gamma_node = Node("gamma")
        gamma_node.left = root.left.right
        gamma_node.right = root.right
        root.right = gamma_node

    elif root.label == "and":
        '''
                    and             =
                     |             / \
                    =++    =>     ,   tau
                    / \           |    |
                   X   E         X++  E++
        '''
        root.label = "="
        comma_node = Node(",")
        tau_node = Node("tau")
        current = root.left
        while current:
            comma_node.left = current.left
            tau_node.left = current.right
            current = current.right
        root.left = comma_node
        root.right = tau_node

    elif root.label == "rec":
        '''
                    rec             =
                     |             / \
                     =     =>     X   gamma
                    / \               /   \
                   X   E            Ystar lambda
                                          /    \
                                         X      E
        '''
        root.label = "="
        gamma_node = Node("gamma")
        y_star_node = Node("<Y*>")
        lambda_node = Node("lambda")
        lambda_node.left = root.left.left
        lambda_node.right = root.left.right
        gamma_node.left = y_star_node
        gamma_node.right = lambda_node
        root.left = root.left.left
        root.right = gamma_node

    return root


if __name__ == "__main__":
    file_name = "Inputs/Q1.txt"
    standardized_tree = standardize(file_name)
    print("Standardized Tree:")
    standardized_tree.print_tree()

# from src.rpal_parser import *

# # The standardize function takes a file name as input and returns a standardized tree.
# def standardize(file_name):
#     ast = parse(file_name)
#     st = make_standardized_tree(ast)
    
#     return st

# # The make_standardized_tree function takes a root node as input and returns a standardized tree.
# def make_standardized_tree(root):
#     for child in root.children:
#         make_standardized_tree(child)

#     if root.value == "let" and root.children[0].value == "=":
#         '''
#                  let                gamma
#                 /   \               /    \    
#                =     P   =>       lambda  E               
#               / \                /     \
#              X   E              X       P
#         '''
#         child_0 = root.children[0]
#         child_1 = root.children[1]

#         root.children[1] = child_0.children[1]
#         root.children[0].children[1] = child_1
#         root.children[0].value = "lambda"
#         root.value = "gamma"

#     elif root.value == "where" and root.children[1].value == "=":
#         '''
#                  where                gamma 
#                  /   \                /    \
#                 E     P     =>      lambda  E
#                      / \             /  \
#                     X   E           X    P
#         '''
#         child_0 = root.children[0] 
#         child_1 = root.children[1] 

#         root.children[0] = child_1.children[1]
#         root.children[1].children[1] = child_0
#         root.children[1].value = "lambda"
#         root.children[0], root.children[1] = root.children[1], root.children[0]
#         root.value = "gamma"

#     elif root.value == "function_form":
#         '''
#                  function_form                  =
#                  /   |    \                    / \
#                 P    V+    E     =>           P   +lambda
#                                                    /   \
#                                                   V    .E                  
#         '''
#         expression = root.children.pop()

#         current_node = root
#         for i in range(len(root.children) - 1):
#             lambda_node = Node("lambda")
#             child = root.children.pop(1)
#             lambda_node.children.append(child)
#             current_node.children.append(lambda_node)
#             current_node = lambda_node

#         current_node.children.append(expression)
#         root.value = "="

#     elif root.value == "gamma" and len(root.children) > 2:
#         expression = root.children.pop()

#         current_node = root
#         for i in range(len(root.children) - 1):
#             lambda_node = Node("lambda")
#             child = root.children.pop(1)
#             lambda_node.children.append(child)
#             current_node.children.append(lambda_node)
#             current_node = lambda_node

#         current_node.children.append(expression)

#     elif root.value == "within" and root.children[0].value == root.children[1].value == "=":
#         '''
#                     within                =
#                     /    \               / \
#                    =      =     =>      X2   gamma
#                   / \    / \                 /   \
#                  X1  E1  X2 E2            lambda  E1 
#                                           /    \
#                                          X1    E2    
#         '''
#         child_0 = root.children[1].children[0]
#         child_1 = Node("gamma")

#         child_1.children.append(Node("lambda"))
#         child_1.children.append(root.children[0].children[1])
#         child_1.children[0].children.append(root.children[0].children[0])
#         child_1.children[0].children.append(root.children[1].children[1])

#         root.children[0] = child_0
#         root.children[1] = child_1
#         root.value = "="

#     elif root.value == "@":
#         '''
#                     @                gamma
#                   / | \              /   \
#                 E1  N  E2    =>    gamma  E2
#                                    /   \
#                                   N     E1
#         '''                
#         expression = root.children.pop(0)
#         identifier = root.children[0]

#         gamma_node = Node("gamma")
#         gamma_node.children.append(identifier)
#         gamma_node.children.append(expression)

#         root.children[0] = gamma_node

#         root.value = "gamma"

#     elif root.value == "and":
#         '''
#                     and             =
#                      |             / \
#                     =++    =>     ,   tau
#                     / \           |    |
#                    X   E         X++  E++
                
#         '''
#         child_0 = Node(",")
#         child_1 = Node("tau")

#         for child in root.children:
#             child_0.children.append(child.children[0])
#             child_1.children.append(child.children[1])

#         root.children.clear()

#         root.children.append(child_0)
#         root.children.append(child_1)

#         root.value = "="

#     elif root.value == "rec":
#         '''
#                     rec             =
#                      |             / \
#                      =     =>     X   gamma
#                     / \               /   \
#                    X   E            Ystar lambda
#                                           /    \
#                                          X      E
#         '''
#         temp = root.children.pop()
#         temp.value = "lambda"

#         gamma_node = Node("gamma")
#         gamma_node.children.append(Node("<Y*>"))
#         gamma_node.children.append(temp)

#         root.children.append(temp.children[0])
#         root.children.append(gamma_node)

#         root.value = "="

#     return root