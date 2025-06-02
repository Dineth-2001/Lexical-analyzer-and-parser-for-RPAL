from scanner.scanner import tokenize_and_screen
import data_structures.enums as enums
from data_structures.node import Node
TokenType = enums.TokenType



# helper function to read the next token and check if it matches the expected type and value
def read(expected_token_type, expected_token):
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token != expected_token or token_type != expected_token_type:
        raise SyntaxError(f"Expected {expected_token} but found {token}")
    else:
        tokens.pop()

# helper function to build the tree structure
def build_tree(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range (0, num_children):
        if stack == []:
            print("Stack is empty")
            exit(1)
        node.children[num_children - i - 1] = stack.pop()
        
    stack.append(node)

# This function parses a list of tokens and builds an abstract syntax tree (AST) from them.
def parse(token_list):
    # Initialize the global variables for tokens and stack
    global tokens
    global stack 
    stack = []
    tokens = token_list
    E()
    if len(tokens) > 0:
        raise SyntaxError("Unexpected tokens at the end of input")
    return stack[0]

def E():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    match tokens[-1][1]:
        case 'let':
            read(TokenType.KEYWORD, 'let')
            D()
            if tokens[-1][1] == 'in':
                read(TokenType.KEYWORD, 'in')
                E()
                build_tree('let', 2)
            else:
                raise SyntaxError("Expected 'in' after 'let'")
        case 'fn':
            read(TokenType.KEYWORD, 'fn')
            n = 0
            while tokens and tokens[-1][1] == '(' or tokens[-1][0] == TokenType.IDENTIFIER:
                Vb()
                n += 1
            if n == 0:
                raise SyntaxError("Expected function parameters after 'fn'")
            
            if tokens and tokens[-1][1] == '.':
                read(TokenType.OPERATOR, '.')
                E()
                build_tree('lambda', n+1)
        case _:
            Ew()

def Ew():
    T()
    if tokens and tokens[-1][1] == 'where':
        read(TokenType.KEYWORD, 'where')
        Dr()
        build_tree('where', 2)

def T():
    Ta()
    n = 0
    while tokens and tokens[-1][1] == ',':
        read(TokenType.PUNCTUATION, ',')
        Ta()
        n += 1
    if n > 0:
        build_tree('tau', n+1)

def Ta():
    Tc()
    while tokens and tokens[-1][1] == 'aug':
        read(TokenType.KEYWORD, 'aug')
        Tc()
        build_tree('aug', 2)

def Tc():
    B()
    if tokens and tokens[-1][1] == '->':
        read(TokenType.OPERATOR, '->')
        Tc()
        token = tokens[-1][1]
        if tokens and token == '|':
            read(TokenType.OPERATOR, '|')
            Tc()
            build_tree('->', 3)
        else:
            raise SyntaxError("Expected '|' after '->'")

def B():
    Bt()
    while tokens and tokens[-1][1] == 'or':
        read(TokenType.KEYWORD, 'or')
        Bt()
        build_tree('or', 2)

def Bt():
    Bs()
    while tokens and tokens[-1][1] == '&':
        read(TokenType.PUNCTUATION, '&')
        Bs()
        build_tree('&', 2)

def Bs():
    if tokens and tokens[-1][1] == 'not':
        read(TokenType.KEYWORD, 'not')
        Bp()
        build_tree('not', 1)
    else:
        Bp()

def Bp():
    A()
    if not tokens:
        return
    token_type, token = tokens[-1]
    if token == 'gr' or token == '>':
        if tokens[-1][1] == 'gr':
            read(TokenType.KEYWORD, 'gr')
        else:
            read(TokenType.OPERATOR, '>')
        A()
        build_tree('gr', 2)
    elif token == 'ge' or token == '>=':
        if tokens[-1][1] == 'ge':
            read(TokenType.KEYWORD, 'ge')
        else:
            read(TokenType.OPERATOR, '>=')
        A()
        build_tree('ge', 2)
    elif token == 'ls' or token == '<':
        if tokens[-1][1] == 'ls':
            read(TokenType.KEYWORD, 'ls')
        else:
            read(TokenType.OPERATOR, '<')
        A()
        build_tree('ls', 2)
    elif token == 'le' or token == '<=':
        if tokens[-1][1] == 'le':
            read(TokenType.KEYWORD, 'le')
        else:
            read(TokenType.OPERATOR, '<=')
        A()
        build_tree('le', 2)
    elif token == 'eq':
        if tokens[-1][1] == 'eq':
            read(TokenType.KEYWORD, 'eq')
        else:
            read(TokenType.OPERATOR, '=')
        A()
        build_tree('eq', 2)
    elif token == 'ne':
        if tokens[-1][1] == 'ne':
            read(TokenType.KEYWORD, 'ne')
        else:
            read(TokenType.OPERATOR, '!=')
        A()
        build_tree('ne', 2)

def A():
    # haddle uniary operators
    if tokens[-1][1] =="+":
        read(TokenType.OPERATOR, '+')
        At()
    elif tokens[-1][1] == "-":
        read(TokenType.OPERATOR, '-')
        At()
        build_tree('neg', 1)
    else:
        At()
    # handle operators with two operands
    while tokens and tokens[-1][1] in ['+', '-']:
        if tokens[-1][1] == '+':
            read(TokenType.OPERATOR, '+')
            At()
            build_tree('+', 2)
        else:
            read(TokenType.OPERATOR, '-')
            At()
            build_tree('-', 2)

def At():
    Af()
    while tokens and tokens[-1][1] in ['*', '/']:
        if tokens[-1][1] == '*':
            read(TokenType.OPERATOR, '*')
            Af()
            build_tree('*', 2)
        else:
            read(TokenType.OPERATOR, '/')
            Af()
            build_tree('/', 2)

def Af():
    Ap()
    while tokens and tokens[-1][1] == '**':
        read(TokenType.OPERATOR, '**')
        Af()
        build_tree('**', 2)

def Ap():
    R()
    while tokens and tokens[-1][1] == '@':
        read(TokenType.OPERATOR, '@')
        if tokens and tokens[-1][0] == TokenType.IDENTIFIER:
            read(TokenType.IDENTIFIER, tokens[-1][1])
            build_tree('<ID:'+ tokens[-1][1] + '>', 0)
            R()
            build_tree('@', 3)
        else:
            raise SyntaxError("Expected identifier after '@'")

def R():
    Rn()
    while tokens and (tokens[-1][0] in [TokenType.IDENTIFIER,TokenType.INTEGER,TokenType.STRING] or
                            tokens[-1][1] in ["true", "false", "nil", "dummy", "("]):
        Rn()
        build_tree('gamma', 2)

def Rn():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+token+'>', 0)
    elif token_type == TokenType.INTEGER:
        read(TokenType.INTEGER, token)
        build_tree('<INT:'+token+'>', 0)
    elif token_type == TokenType.STRING:
        read(TokenType.STRING, token)
        build_tree('<STR:\''+token+'\'>', 0)
    elif token == 'true':
        read(TokenType.KEYWORD, 'true')
        build_tree('<true>', 0)
    elif token == 'false':
        read(TokenType.KEYWORD, 'false')
        build_tree('<false>', 0)
    elif token == 'nil':
        read(TokenType.KEYWORD, 'nil')
        build_tree('<nil>', 0)
    elif token == '(':
        read(TokenType.PUNCTUATION , '(')
        E()
        read(TokenType.PUNCTUATION, ')')
    elif token == 'dummy':
        read(TokenType.KEYWORD, 'dummy')
        build_tree('<dummy>', 0)
    else:
        raise SyntaxError(f"Unexpected token {token}")

def D():
    Da()
    if tokens and tokens[-1][1] == 'within':
        read(TokenType.KEYWORD, 'within')
        D()
        build_tree('within', 2)

def Da():
    Dr()
    n = 0
    while tokens and tokens[-1][1] == 'and':
        read(TokenType.KEYWORD, 'and')
        Dr()
        n += 1
    if n > 0:
        build_tree('and', n+1)

def Dr():
    if tokens and tokens[-1][1] == 'rec':
        read(TokenType.KEYWORD, 'rec')
        Db()
        build_tree('rec', 1)
    else:
        Db()

def Db():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)

        if tokens and tokens[-1][1] in  ['=',',']:
            Vl()
            read(TokenType.OPERATOR, '=')
            E()
            build_tree('=', 2)
        else:
            n= 0
            while tokens[-1][0] == TokenType.IDENTIFIER or tokens[-1][1] == '(':
                Vb()
                n += 1
            if n == 0:
                raise SyntaxError("Expected identifier or '(' after identifier")
            if tokens and tokens[-1][1] == '=':
                read(TokenType.OPERATOR, '=')
                E()
                build_tree('function_form', n+2)
            else:
                raise SyntaxError("Expected '=' after identifier")
    elif token_type == TokenType.PUNCTUATION and token == '(':
        read( TokenType.PUNCTUATION, '(')
        D()
        read(TokenType.PUNCTUATION, ')')

def Vb():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)

    elif token == '(':
        read(TokenType.PUNCTUATION, '(')

        token_type, token = tokens[-1]
        if token_type == TokenType.PUNCTUATION and token == ')':
            read(TokenType.PUNCTUATION, ')')
            build_tree('()', 0)
        elif token_type == TokenType.IDENTIFIER:
            read(TokenType.IDENTIFIER, token)
            build_tree('<ID:'+ token + '>', 0)
            Vl()
            if tokens and tokens[-1][1] == ')':
                read(TokenType.PUNCTUATION, ')')   
            else:
                raise SyntaxError("Expected ')' after identifier")
        else:
            raise SyntaxError("Expected identifier or ')' after '('")
    else:
        raise SyntaxError(f"Unexpected token {token}")
        
def Vl():
    n = 0
    while tokens and tokens[-1][1] == ',':
        read(TokenType.PUNCTUATION, ',')
        if not tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = tokens[-1]
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)
        n += 1

    if n > 0:
        build_tree(',', n+1)

if __name__ == "__main__":
    with open('Inputs/Q3.txt', 'r') as file:
        code = file.read()
        tokens = tokenize_and_screen(code)

        # Reverse the tokens so that we can use the list as a stack,
        # where popping from the front (index 0) simulates popping from the top of the original token sequence
        tokens.reverse()
 
        ast = parse(tokens)

        ast.print_tree()

    

   