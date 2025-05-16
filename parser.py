from scanner import Scanner
import token_types

token_types = token_types.TokenType

class Node:
    def __init__(self, label):
        self.label = label
        self.left = None
        self.right = None

    def print_tree(self, level=0):
        print('.' * level + str(self.label))
        if self.left:
            self.left.print_tree(level + 1)
        if self.right:
            self.right.print_tree(level)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []

    def read(self, expected_token_type, expected_token):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token != expected_token or token_type != expected_token_type:
            raise SyntaxError(f"Expected {expected_token} but found {token}")
        else:
            self.tokens.pop()

    def build_tree(self, x, n):
        parent = Node(x)
        
        if n > 0:
            children = self.stack[-n:]
            self.stack = self.stack[:-n]
            parent.left = children[0]
            cursor = parent.left
            for child in children[1:]:
                cursor.right = child
                cursor = child

        self.stack.append(parent)
        # print("###########################################################")
        # for i in self.stack:
        #     i.print_tree()
        #     print("---------------------------------------------------------")  

    def parse(self):
        self.E()
        if len(self.tokens) > 0:
            raise SyntaxError("Unexpected tokens at the end of input")
        return self.stack[0]

    def E(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        match self.tokens[-1][1]:
            case 'let':
                self.read(token_types.KEYWORD, 'let')
                self.D()
                if self.tokens[-1][1] == 'in':
                    self.read(token_types.KEYWORD, 'in')
                    self.E()
                    self.build_tree('let', 2)
                else:
                    raise SyntaxError("Expected 'in' after 'let'")
            case 'fn':
                self.read(token_types.KEYWORD, 'fn')
                n = 0
                while self.tokens and self.tokens[-1][1] == '(' or self.tokens[-1][0] == token_types.IDENTIFIER:
                    self.Vb()
                    n += 1
                if n == 0:
                    raise SyntaxError("Expected function parameters after 'fn'")
                
                if self.tokens and self.tokens[-1][1] == '.':
                    self.read(token_types.OPERATOR, '.')
                    self.E()
                    self.build_tree('lambda', n+1)
            case _:
                self.Ew()

    def Ew(self):
        self.T()
        if self.tokens and self.tokens[-1][1] == 'where':
            self.read(token_types.KEYWORD, 'where')
            self.Dr()
            self.build_tree('where', 2)

    def T(self):
        self.Ta()
        n = 0
        while self.tokens and self.tokens[-1][1] == ',':
            self.read(token_types.PUNCTUATION, ',')
            self.Ta()
            n += 1
        if n > 0:
            self.build_tree('tau', n+1)

    def Ta(self):
        self.Tc()
        while self.tokens and self.tokens[-1][1] == 'aug':
            self.read(token_types.KEYWORD, 'aug')
            self.Tc()
            self.build_tree('aug', 2)

    def Tc(self):
        self.B()
        if self.tokens and self.tokens[-1][1] == '->':
            self.read(token_types.OPERATOR, '->')
            self.Tc()
            token = self.tokens[-1][1]
            if self.tokens and token == '|':
                self.read(token_types.OPERATOR, '|')
                self.Tc()
                self.build_tree('->', 3)
            else:
                raise SyntaxError("Expected '|' after '->'")

    def B(self):
        self.Bt()
        while self.tokens and self.tokens[-1][1] == 'or':
            self.read(token_types.KEYWORD, 'or')
            self.Bt()
            self.build_tree('or', 2)

    def Bt(self):
        self.Bs()
        while self.tokens and self.tokens[-1][1] == '&':
            self.read(token_types.PUNCTUATION, '&')
            self.Bs()
            self.build_tree('&', 2)

    def Bs(self):
        if self.tokens and self.tokens[-1][1] == 'not':
            self.read(token_types.KEYWORD, 'not')
            self.Bp()
            self.build_tree('not', 1)
        else:
            self.Bp()

    def Bp(self):
        self.A()
        if not self.tokens:
            return
        token_type, token = self.tokens[-1]
        if token == 'gr' or token == '>':
            if self.tokens[-1][1] == 'gr':
                self.read(token_types.KEYWORD, 'gr')
            else:
                self.read(token_types.OPERATOR, '>')
            self.A()
            self.build_tree('gr', 2)
        elif token == 'ge' or token == '>=':
            if self.tokens[-1][1] == 'ge':
                self.read(token_types.KEYWORD, 'ge')
            else:
                self.read(token_types.OPERATOR, '>=')
            self.A()
            self.build_tree('ge', 2)
        elif token == 'ls' or token == '<':
            if self.tokens[-1][1] == 'ls':
                self.read(token_types.KEYWORD, 'ls')
            else:
                self.read(token_types.OPERATOR, '<')
            self.A()
            self.build_tree('ls', 2)
        elif token == 'le' or token == '<=':
            if self.tokens[-1][1] == 'le':
                self.read(token_types.KEYWORD, 'le')
            else:
                self.read(token_types.OPERATOR, '<=')
            self.A()
            self.build_tree('le', 2)
        elif token == 'eq':
            if self.tokens[-1][1] == 'eq':
                self.read(token_types.KEYWORD, 'eq')
            else:
                self.read(token_types.OPERATOR, '=')
            self.A()
            self.build_tree('eq', 2)
        elif token == 'ne':
            if self.tokens[-1][1] == 'ne':
                self.read(token_types.KEYWORD, 'ne')
            else:
                self.read(token_types.OPERATOR, '!=')
            self.A()
            self.build_tree('ne', 2)

    def A(self):
        # haddle uniary operators
        if self.tokens[-1][1] =="+":
            self.read(token_types.OPERATOR, '+')
            self.At()
        elif self.tokens[-1][1] == "-":
            self.read(token_types.OPERATOR, '-')
            self.At()
            self.build_tree('neg', 1)
        else:
            self.At()
        # handle operators with two operands
        while self.tokens and self.tokens[-1][1] in ['+', '-']:
            if self.tokens[-1][1] == '+':
                self.read(token_types.OPERATOR, '+')
                self.At()
                self.build_tree('+', 2)
            else:
                self.read(token_types.OPERATOR, '-')
                self.At()
                self.build_tree('-', 2)

    def At(self):
        self.Af()
        while self.tokens and self.tokens[-1][1] in ['*', '/']:
            if self.tokens[-1][1] == '*':
                self.read(token_types.OPERATOR, '*')
                self.Af()
                self.build_tree('*', 2)
            else:
                self.read(token_types.OPERATOR, '/')
                self.Af()
                self.build_tree('/', 2)

    def Af(self):
        self.Ap()
        while self.tokens and self.tokens[-1][1] == '**':
            self.read(token_types.OPERATOR, '**')
            self.Af()
            self.build_tree('**', 2)

    def Ap(self):
        self.R()
        while self.tokens and self.tokens[-1][1] == '@':
            self.read(token_types.OPERATOR, '@')
            if self.tokens and self.tokens[-1][0] == token_types.IDENTIFIER:
                self.read(token_types.IDENTIFIER, self.tokens[-1][1])
                self.build_tree('<ID:'+ self.tokens[-1][1] + '>', 0)
                self.R()
                self.build_tree('@', 3)
            else:
                raise SyntaxError("Expected identifier after '@'")

    def R(self):
        self.Rn()
        while self.tokens and (self.tokens[-1][0] in [token_types.IDENTIFIER,token_types.INTEGER,token_types.STRING] or
                               self.tokens[-1][1] in ["true", "false", "nil", "dummy", "("]):
            self.Rn()
            self.build_tree('gamma', 2)

    def Rn(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        print(token_type, token)
        if token_type == token_types.IDENTIFIER:
            self.read(token_types.IDENTIFIER, token)
            self.build_tree('<ID:'+token+'>', 0)
        elif token_type == token_types.INTEGER:
            self.read(token_types.INTEGER, token)
            self.build_tree('<INT:'+token+'>', 0)
        elif token_type == token_types.STRING:
            self.read(token_types.STRING, token)
            self.build_tree('<STR:\''+token+'\'>', 0)
        elif token == 'true':
            self.read(token_types.KEYWORD, 'true')
            self.build_tree('true', 0)
        elif token == 'false':
            self.read(token_types.KEYWORD, 'false')
            self.build_tree('false', 0)
        elif token == 'nil':
            self.read(token_types.KEYWORD, 'nil')
            self.build_tree('nil', 0)
        elif token == '(':
            self.read(token_types.PUNCTUATION , '(')
            self.E()
            self.read(token_types.PUNCTUATION, ')')
        elif token == 'dummy':
            self.read(token_types.KEYWORD, 'dummy')
            self.build_tree('dummy', 0)
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def D(self):
        self.Da()
        if self.tokens and self.tokens[-1][1] == 'within':
            self.read(token_types.KEYWORD, 'within')
            self.D()
            self.build_tree('within', 2)

    def Da(self):
        self.Dr()
        n = 0
        while self.tokens and self.tokens[-1][1] == 'and':
            self.read(token_types.KEYWORD, 'and')
            self.Dr()
            n += 1
        if n > 0:
            self.build_tree('and', n+1)

    def Dr(self):
        if self.tokens and self.tokens[-1][1] == 'rec':
            self.read(token_types.KEYWORD, 'rec')
            self.Db()
            self.build_tree('rec', 1)
        else:
            self.Db()

    def Db(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token_type == token_types.IDENTIFIER:
            self.read(token_types.IDENTIFIER, token)
            self.build_tree('<ID:'+ token + '>', 0)

            if self.tokens and self.tokens[-1][1] in  ['=',',']:
                self.Vl()
                self.read(token_types.OPERATOR, '=')
                self.E()
                self.build_tree('=', 2)
            else:
                n= 0
                while self.tokens[-1][0] == token_types.IDENTIFIER or self.tokens[-1][1] == '(':
                    self.Vb()
                    n += 1
                if n == 0:
                    raise SyntaxError("Expected identifier or '(' after identifier")
                if self.tokens and self.tokens[-1][1] == '=':
                    self.read(token_types.OPERATOR, '=')
                    self.E()
                    self.build_tree('function_form', n+2)
                else:
                    raise SyntaxError("Expected '=' after identifier")
        elif token_type == token_types.PUNCTUATION and token == '(':
            self.read( token_types.PUNCTUATION, '(')
            self.D()
            self.read(token_types.PUNCTUATION, ')')

    def Vb(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token_type == token_types.IDENTIFIER:
            self.read(token_types.IDENTIFIER, token)
            self.build_tree('<ID:'+ token + '>', 0)

        elif token == '(':
            self.read(token_types.PUNCTUATION, '(')

            token_type, token = self.tokens[-1]
            if token_type == token_types.PUNCTUATION and token == ')':
                self.read(token_types.PUNCTUATION, ')')
                self.build_tree('()', 0)
            elif token_type == token_types.IDENTIFIER:
                self.read(token_types.IDENTIFIER, token)
                self.build_tree('<ID:'+ token + '>', 0)
                self.Vl()
                if self.tokens and self.tokens[-1][1] == ')':
                    self.read(token_types.PUNCTUATION, ')')   
                else:
                    raise SyntaxError("Expected ')' after identifier")
            else:
                raise SyntaxError("Expected identifier or ')' after '('")
        else:
            raise SyntaxError(f"Unexpected token {token}")
           
    def Vl(self):
        n = 0
        while self.tokens and self.tokens[-1][1] == ',':
            self.read(token_types.PUNCTUATION, ',')
            if not self.tokens:
                raise SyntaxError("Unexpected end of input")
            token_type, token = self.tokens[-1]
            self.read(token_types.IDENTIFIER, token)
            self.build_tree('<ID:'+ token + '>', 0)
            n += 1

        if n > 0:
            self.build_tree(',', n+1)

if __name__ == "__main__":
    scaner = Scanner()
    with open('Inputs\Q8.txt', 'r') as file:
        code = file.read()
        tokens = scaner.tokenize(code)
        for i in tokens: print(i)
        tokens.reverse()
        parser = Parser(tokens)
        parser.parse()
        parser.stack[0].print_tree()
    
   