from scanner.scanner import tokenize_and_screen
import data_structures.enums as enums
from data_structures.node import Node
TokenType = enums.TokenType

# Helper function to read the next token and check if it matches the expected type and value
def read(expected_token_type, expected_token):
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token != expected_token or token_type != expected_token_type:
        raise SyntaxError(f"Expected {expected_token} but found {token}")
    else:
        tokens.pop()

# Helper function to build the tree structure
# Pops children from the stack in reverse order to maintain correct structure
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
    E()   # Start parsing with the Expression non-terminal
    if len(tokens) > 0:
        raise SyntaxError("Unexpected tokens at the end of input")
    return stack[0]

# Handles 'let', 'fn', and other expressions 
def E():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    match tokens[-1][1]:
        case 'let':  # Rule: E -> 'let' D 'in' E => 'let'
            read(TokenType.KEYWORD, 'let')
            D()
            if tokens[-1][1] == 'in':
                read(TokenType.KEYWORD, 'in')
                E()
                build_tree('let', 2)  # Build 'let' node with D and E as children
            else:
                raise SyntaxError("Expected 'in' after 'let'")
        case 'fn':  # Rule: E -> 'fn' Vb+ '.' E => 'lambda'
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
                build_tree('lambda', n+1)  # Build 'lambda' node with Vb(s) and E as children
        case _:
            Ew()

# Rule: Ew -> T 'where' Dr => 'where' 
#          -> T
def Ew():
    T()
    if tokens and tokens[-1][1] == 'where':
        read(TokenType.KEYWORD, 'where')
        Dr()
        build_tree('where', 2)  # Build 'where' node with T and Dr as children

# Rule: T -> Ta (',' Ta )+ => 'tau' 
#         -> Ta
def T():
    Ta()
    n = 0
    while tokens and tokens[-1][1] == ',':
        read(TokenType.PUNCTUATION, ',')
        Ta()
        n += 1
    if n > 0:
        build_tree('tau', n+1)  # Build 'tau' node for comma-separated expressions

# Rule: Ta -> Tc 'aug' Ta => 'aug' 
#          -> Tc
def Ta():
    Tc()
    while tokens and tokens[-1][1] == 'aug':
        read(TokenType.KEYWORD, 'aug')
        Tc()
        build_tree('aug', 2)  # Build 'aug' node with two Tc children

# Rule: Tc -> B '->' Tc '|' Tc => '->' 
#          -> B
def Tc():
    B()
    if tokens and tokens[-1][1] == '->':
        read(TokenType.OPERATOR, '->')
        Tc()  # Parse then-branch
        token = tokens[-1][1]
        if tokens and token == '|':
            read(TokenType.OPERATOR, '|')
            Tc()  # Parse else-branch
            build_tree('->', 3)  # Build '->' node with B, then, and else branches
        else:
            raise SyntaxError("Expected '|' after '->'")

# Rule: B -> Bt 'or' Bt => 'or' 
#         -> Bt
def B():
    Bt()
    while tokens and tokens[-1][1] == 'or':
        read(TokenType.KEYWORD, 'or')
        Bt()
        build_tree('or', 2)  # Build 'or' node with two Bt children

# Rule: Bt -> Bs '&' Bs => '&' 
#          -> Bs
def Bt():
    Bs()
    while tokens and tokens[-1][1] == '&':
        read(TokenType.PUNCTUATION, '&')
        Bs()
        build_tree('&', 2)  # Build '&' node with two Bs children

# Rule: Bs -> 'not' Bp => 'not'
#          -> Bp
def Bs():
    if tokens and tokens[-1][1] == 'not':
        read(TokenType.KEYWORD, 'not')
        Bp()
        build_tree('not', 1)  # Build 'not' node with one Bp child
    else:
        Bp()

# Handles comparison operators: 'gr', 'ge', 'ls', 'le', 'eq', 'ne'
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

# Handles unary '+' (ignored), unary '-', and binary '+' or '-' operators
def A():
    # Handle unary operators
    if tokens[-1][1] =="+":
        read(TokenType.OPERATOR, '+')  
        At()
    elif tokens[-1][1] == "-":
        read(TokenType.OPERATOR, '-')
        At() 
        build_tree('neg', 1)  # Build 'neg' node for unary minus
    else:
        At()
    # Handle binary operators
    while tokens and tokens[-1][1] in ['+', '-']:
        if tokens[-1][1] == '+':
            read(TokenType.OPERATOR, '+')
            At()
            build_tree('+', 2)  # Build '+' node with two children
        else:
            read(TokenType.OPERATOR, '-')
            At()
            build_tree('-', 2)  # Build '-' node with two children

# Rule: At -> Af ('*' | '/') Af => '*' | '/' 
#          -> Af
def At():
    Af()
    while tokens and tokens[-1][1] in ['*', '/']:
        if tokens[-1][1] == '*':
            read(TokenType.OPERATOR, '*')
            Af()
            build_tree('*', 2)  # Build '*' node with two children
        else:
            read(TokenType.OPERATOR, '/')
            Af()
            build_tree('/', 2)  # Build '/' node with two children

# Rule: Af -> Ap '**' Af => '**'
#          -> Ap
def Af():
    Ap()
    while tokens and tokens[-1][1] == '**':
        read(TokenType.OPERATOR, '**')
        Af()
        build_tree('**', 2)  # Build '**' node with two children

# Rule: Ap -> R '@' <IDENTIFIER> R => '@' | R
def Ap():
    R()
    while tokens and tokens[-1][1] == '@':
        read(TokenType.OPERATOR, '@')
        if tokens and tokens[-1][0] == TokenType.IDENTIFIER:
            read(TokenType.IDENTIFIER, tokens[-1][1])
            build_tree('<ID:'+ tokens[-1][1] + '>', 0)
            R()
            build_tree('@', 3)  # Build '@' node with R, identifier, and R as children
        else:
            raise SyntaxError("Expected identifier after '@'")

# Rule: R -> Rn Rn => 'gamma'
#          -> Rn
def R():
    Rn()
    while tokens and (tokens[-1][0] in [TokenType.IDENTIFIER,TokenType.INTEGER,TokenType.STRING] or
                            tokens[-1][1] in ["true", "false", "nil", "dummy", "("]):
        Rn()
        build_tree('gamma', 2)  # Build 'gamma' node with two Rn children for function application

# Handles identifiers, integers, strings, booleans, nil, dummy, and parenthesized expressions
def Rn():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+token+'>', 0)  # Build identifier node
    elif token_type == TokenType.INTEGER:
        read(TokenType.INTEGER, token)
        build_tree('<INT:'+token+'>', 0)  # Build integer node
    elif token_type == TokenType.STRING:
        read(TokenType.STRING, token)
        build_tree('<STR:\''+token+'\'>', 0)  # Build string node
    elif token == 'true':
        read(TokenType.KEYWORD, 'true')
        build_tree('<true>', 0)  # Build boolean true node
    elif token == 'false':
        read(TokenType.KEYWORD, 'false')
        build_tree('<false>', 0)  # Build boolean false node
    elif token == 'nil':
        read(TokenType.KEYWORD, 'nil')
        build_tree('<nil>', 0)  # Build nil node
    elif token == '(':
        read(TokenType.PUNCTUATION , '(')
        E()
        read(TokenType.PUNCTUATION, ')')
    elif token == 'dummy':
        read(TokenType.KEYWORD, 'dummy')
        build_tree('<dummy>', 0)  # Build dummy node
    else:
        raise SyntaxError(f"Unexpected token {token}")

# Rule: D -> Da 'within' D => 'within'
#         -> Da
def D():
    Da()
    if tokens and tokens[-1][1] == 'within':
        read(TokenType.KEYWORD, 'within')
        D()
        build_tree('within', 2)  # Build 'within' node with Da and D as children

# Rule: Da -> Dr ('and' Dr )+ => 'and' 
#          -> Dr
def Da():
    Dr()
    n = 0
    while tokens and tokens[-1][1] == 'and':
        read(TokenType.KEYWORD, 'and')
        Dr()
        n += 1
    if n > 0:
        build_tree('and', n+1)  # Build 'and' node for multiple definitions

# Rule: Dr -> 'rec' Db => 'rec' 
#          -> Db
def Dr():
    if tokens and tokens[-1][1] == 'rec':
        read(TokenType.KEYWORD, 'rec')
        Db()
        build_tree('rec', 1)  # Build 'rec' node with Db as child
    else:
        Db()

# Rules: Db -> <IDENTIFIER> Vl '=' E => '=' | <IDENTIFIER> Vb+ '=' E => 'function_form' | '(' D ')'
def Db():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)  # Build identifier node

        if tokens and tokens[-1][1] in  ['=',',']:
            Vl()  # Parse variable list
            read(TokenType.OPERATOR, '=')
            E()
            build_tree('=', 2)  # Build '=' node for simple binding
        else:
            n= 0
            while tokens[-1][0] == TokenType.IDENTIFIER or tokens[-1][1] == '(':
                Vb()  # Parse variable bindings
                n += 1
            if n == 0:
                raise SyntaxError("Expected identifier or '(' after identifier")
            if tokens and tokens[-1][1] == '=':
                read(TokenType.OPERATOR, '=')
                E()
                build_tree('function_form', n+2)  # Build 'function_form' node
            else:
                raise SyntaxError("Expected '=' after identifier")
    elif token_type == TokenType.PUNCTUATION and token == '(':
        read( TokenType.PUNCTUATION, '(')
        D()
        read(TokenType.PUNCTUATION, ')')

# Rules: Vb -> <IDENTIFIER> | '(' <IDENTIFIER> Vl ')' | '(' ')'
def Vb():
    if not tokens:
        raise SyntaxError("Unexpected end of input")
    token_type, token = tokens[-1]
    if token_type == TokenType.IDENTIFIER:
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)  # Build identifier node

    elif token == '(':
        read(TokenType.PUNCTUATION, '(')

        token_type, token = tokens[-1]
        if token_type == TokenType.PUNCTUATION and token == ')':
            read(TokenType.PUNCTUATION, ')')
            build_tree('()', 0)  # Build empty tuple node
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

# Rule: Vl -> (',' <IDENTIFIER>)+ => ',' | ε        
def Vl():
    n = 0
    while tokens and tokens[-1][1] == ',':
        read(TokenType.PUNCTUATION, ',')
        if not tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = tokens[-1]
        read(TokenType.IDENTIFIER, token)
        build_tree('<ID:'+ token + '>', 0)  # Build identifier node
        n += 1

    if n > 0:
        build_tree(',', n+1)  # Build ',' node for variable list

if __name__ == "__main__":
    with open('Inputs/Q3.txt', 'r') as file:
        code = file.read()
        tokens = tokenize_and_screen(code)

        # Reverse the tokens so that we can use the list as a stack,
        # where popping from the front (index 0) simulates popping from the top of the original token sequence
        tokens.reverse()
 
        ast = parse(tokens)

        ast.print_tree()

    

   