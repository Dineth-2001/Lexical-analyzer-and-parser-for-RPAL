from data_structures.node import Node
from scanner.scanner import tokenize_and_screen
from parser.parser import parse


# Takes a root node as input and returns a standardized tree.
def generate_standardized_tree(node):
    idx = 0
    while idx < len(node.children):
        generate_standardized_tree(node.children[idx])
        idx += 1

    if node.value == "let" and node.children[0].value == "=":
        '''
                 let                gamma
                /   \               /    \    
               =     P   =>       lambda  E               
              / \                /     \
             X   E              X       P
        '''
        assign_node = node.children[0]
        expr_node = node.children[1]

        node.children[1] = assign_node.children[1]
        assign_node.children[1] = expr_node
        assign_node.value = "lambda"
        node.value = "gamma"

    elif node.value == "where" and node.children[1].value == "=":
        '''
                 where                gamma 
                 /   \                /    \
                E     P     =>      lambda  E
                     / \             /  \
                    X   E           X    P
        '''
        expr = node.children[0]
        assign_node = node.children[1]

        node.children[0] = assign_node.children[1]
        assign_node.children[1] = expr
        assign_node.value = "lambda"
        node.children[0], node.children[1] = node.children[1], node.children[0]
        node.value = "gamma"

    elif node.value == "function_form":
        '''
                 function_form                  =
                 /   |    \                    / \
                P    V+    E     =>           P   +lambda
                                                   /   \
                                                  V    .E                  
        '''
        final_expr = node.children.pop()
        current = node
        remaining_vars = len(node.children) - 1
        arg_index = 1

        while remaining_vars > 0:
            lambda_node = Node("lambda")
            argument = node.children.pop(arg_index)
            lambda_node.children.append(argument)
            current.children.append(lambda_node)
            current = lambda_node
            remaining_vars -= 1

        current.children.append(final_expr)
        node.value = "="

    elif node.value == "gamma" and len(node.children) > 2:
        final_expr = node.children.pop()
        current = node
        remaining_args = len(node.children) - 1
        arg_index = 1

        while remaining_args > 0:
            lambda_node = Node("lambda")
            argument = node.children.pop(arg_index)
            lambda_node.children.append(argument)
            current.children.append(lambda_node)
            current = lambda_node
            remaining_args -= 1

        current.children.append(final_expr)

    elif node.value == "within" and node.children[0].value == node.children[1].value == "=":
        '''
                    within                =
                    /    \               / \
                   =      =     =>      X2   gamma
                  / \    / \                 /   \
                 X1  E1  X2 E2            lambda  E1 
                                          /    \
                                         X1    E2    
        '''
        inner_var = node.children[1].children[0]

        gamma_expr = Node("gamma")
        lambda_expr = Node("lambda")

        lambda_expr.children.append(node.children[0].children[0])
        lambda_expr.children.append(node.children[1].children[1])
        gamma_expr.children.append(Node("<Y*>"))
        gamma_expr.children.append(lambda_expr)

        node.children[0] = inner_var
        node.children[1] = gamma_expr
        node.value = "="

    elif node.value == "@":
        '''
                    @                gamma
                  / | \              /   \
                E1  N  E2    =>    gamma  E2
                                   /   \
                                  N     E1
        ''' 
        right_expr = node.children.pop(0)
        left_node = node.children[0]

        gamma_expr = Node("gamma")
        gamma_expr.children.append(left_node)
        gamma_expr.children.append(right_expr)

        node.children[0] = gamma_expr
        node.value = "gamma"

    elif node.value == "and":
        '''
                    and             =
                     |             / \
                    =++    =>     ,   tau
                    / \           |    |
                   X   E         X++  E++
                
        '''
        tuple_node = Node(",")
        tau_node = Node("tau")

        idx = 0
        while idx < len(node.children):
            assignment = node.children[idx]
            tuple_node.children.append(assignment.children[0])
            tau_node.children.append(assignment.children[1])
            idx += 1

        node.children.clear()
        node.children.append(tuple_node)
        node.children.append(tau_node)
        node.value = "="

    elif node.value == "rec":
        '''
                    rec             =
                     |             / \
                     =     =>     X   gamma
                    / \               /   \
                   X   E            Ystar lambda
                                          /    \
                                         X      E
        '''
        assignment = node.children.pop()
        assignment.value = "lambda"

        gamma_expr = Node("gamma")
        gamma_expr.children.append(Node("<Y*>"))
        gamma_expr.children.append(assignment)

        node.children.append(assignment.children[0])
        node.children.append(gamma_expr)
        node.value = "="

    return node

if __name__ == "__main__":
    with open('Inputs/Q6.txt', 'r') as file:
        code = file.read()
        tokens = tokenize_and_screen(code)

        # Reverse the tokens so that we can use the list as a stack,
        # where popping from the front (index 0) simulates popping from the top of the original token sequence
        tokens.reverse()
 
        ast = parse(tokens)
        standardized_tree = generate_standardized_tree(ast)
        print("Standardized Tree:")
        standardized_tree.print_tree()
        print("========================================")

