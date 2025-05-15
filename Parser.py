from scanner import Scanner

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
                self.read('KEYWORD', 'let')
                self.D()
                self.read('KEYWORD', 'in')
                self.E()
                self.build_tree('let', 2)
            case 'fn':
                self.read('KEYWORD', 'fn')
                n = 1
                while self.tokens and self.tokens[-1][1] == '(' or self.tokens[-1][0] == 'IDENTIFIER':
                    self.Vb()
                    n += 1
                self.read('OPERATOR', '.')
                self.E()
                self.build_tree('fn', n)
            case _:
                self.Ew()

    def Ew(self):
        self.T()
        if self.tokens and self.tokens[-1][1] == 'where':
            self.read('KEYWORD', 'where')
            self.Dr()
            self.build_tree('where', 2)

    def T(self):
        self.Ta()
        n = 1
        while self.tokens and self.tokens[-1][1] == ',':
            self.read('PUNCTUATION', ',')
            self.Ta()
            n += 1
        if n > 1:
            self.build_tree('tau', n)

    def Ta(self):
        self.Tc()
        while self.tokens and self.tokens[-1][1] == 'aug':
            self.read('KEYWORD', 'aug')
            self.Tc()
            self.build_tree('aug', 2)

    def Tc(self):
        self.B()
        if self.tokens and self.tokens[-1][1] == '->':
            self.read('OPERATOR', '->')
            self.Tc()
            self.read('OPERATOR', '|')
            self.Tc()
            self.build_tree('->', 3)

    def B(self):
        self.Bt()
        while self.tokens and self.tokens[-1][1] == 'or':
            self.read('KEYWORD', 'or')
            self.Bt()
            self.build_tree('or', 2)

    def Bt(self):
        self.Bs()
        while self.tokens and self.tokens[-1][1] == '&':
            self.read('PUNCTUATION', '&')
            self.Bs()
            self.build_tree('&', 2)

    def Bs(self):
        if self.tokens and self.tokens[-1][1] == 'not':
            self.read('KEYWORD', 'not')
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
            self.read('KEYWORD', 'gr')
            self.A()
            self.build_tree('gr', 2)
        elif token == 'ge' or token == '>=':
            self.read('KEYWORD', 'ge')
            self.A()
            self.build_tree('ge', 2)
        elif token == 'ls' or token == '<':
            self.read('KEYWORD', 'ls')
            self.A()
            self.build_tree('ls', 2)
        elif token == 'le' or token == '<=':
            self.read('KEYWORD', 'le')
            self.A()
            self.build_tree('le', 2)
        elif token == 'eq':
            self.read('KEYWORD', 'eq')
            self.A()
            self.build_tree('eq', 2)
        elif token == 'ne':
            self.read('KEYWORD', 'ne')
            self.A()
            self.build_tree('ne', 2)

    def A(self):
        # haddle uniary operators
        if self.tokens[-1][1] =="+":
            self.read('OPERATOR', '+')
            self.At()
        elif self.tokens[-1][1] == "-":
            self.read('OPERATOR', '-')
            self.At()
            self.build_tree('neg', 2)
        else:
            self.At()
        # handle operators with two operands
        while self.tokens and self.tokens[-1][1] in ['+', '-']:
            if self.tokens[-1][1] == '+':
                self.read('PUNCTUATION', '+')
                self.At()
                self.build_tree('+', 2)
            else:
                self.read('PUNCTUATION', '-')
                self.At()
                self.build_tree('-', 2)

    def At(self):
        self.Af()
        while self.tokens and self.tokens[-1][1] in ['*', '/']:
            if self.tokens[-1][1] == '*':
                self.read('PUNCTUATION', '*')
                self.Af()
                self.build_tree('*', 2)
            else:
                self.read('PUNCTUATION', '/')
                self.Af()
                self.build_tree('/', 2)

    def Af(self):
        self.Ap()
        while self.tokens and self.tokens[-1][1] == '**':
            self.read('PUNCTUATION', '**')
            self.Af()
            self.build_tree('**', 2)

    def Ap(self):
        self.R()
        while self.tokens and self.tokens[-1][1] == '@':
            self.read('PUNCTUATION', '@')
            self.read('IDENTIFIER', self.tokens[-1][1])
            self.build_tree('IDENTIFIER', 0)
            self.R()
            self.build_tree('@', 3)

    def R(self):
        self.Rn()
        while self.tokens and (self.tokens[-1][0] in ["IDENTIFIER", "INTEGER", "STRING"] or
                               self.tokens[-1][1] in ["true", "false", "nil", "dummy", "("]):
            self.Rn()
            self.build_tree('gamma', 2)

    def Rn(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token_type == 'IDENTIFIER':
            self.read('IDENTIFIER', token)
            self.build_tree('IDENTIFIER', 0)
        elif token_type == 'INTEGER':
            self.read('INTEGER', token)
            self.build_tree('INTEGER', 0)
        elif token_type == 'STRING':
            self.read('STRING', token)
            self.build_tree('STRING', 0)
        elif token == 'true':
            self.read('KEYWORD', 'true')
            self.build_tree('true', 0)
        elif token == 'false':
            self.read('KEYWORD', 'false')
            self.build_tree('false', 0)
        elif token == 'nil':
            self.read('KEYWORD', 'nil')
            self.build_tree('nil', 0)
        elif token == '(':
            self.read('PUNCTUATION', '(')
            self.E()
            self.read('PUNCTUATION', ')')
        elif token == 'dummy':
            self.read('KEYWORD', 'dummy')
            self.build_tree('dummy', 0)
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def D(self):
        self.Da()
        if self.tokens and self.tokens[-1][1] == 'within':
            self.read('KEYWORD', 'within')
            self.D()
            self.build_tree('within', 2)

    def Da(self):
        self.Dr()
        n = 1
        while self.tokens and self.tokens[-1][1] == 'and':
            self.read('KEYWORD', 'and')
            self.Dr()
            n += 1
        if n > 1:
            self.build_tree('and', n)

    def Dr(self):
        if self.tokens and self.tokens[-1][1] == 'rec':
            self.read('KEYWORD', 'rec')
            self.Db()
            self.build_tree('rec', 1)
        else:
            self.Db()

    def Db(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token_type == 'IDENTIFIER':
            self.read('IDENTIFIER', token)
            self.build_tree('IDENTIFIER', 0)
            n = 1
            while self.tokens and self.tokens[-1][1] != '=':
                self.Vb()
                n += 1
            self.read('OPERATOR', '=')
            self.E()
            self.build_tree('fcn_form', 2)
        elif token_type == 'PUNCTUATION' and token == '(':
            self.read('PUNCTUATION', '(')
            self.D()
            self.read('PUNCTUATION', ')')
        else:
            self.v1()
            self.read('OPERATOR', '=')
            self.E()
            self.build_tree('=', 2)

    def Vb(self):
        if not self.tokens:
            raise SyntaxError("Unexpected end of input")
        token_type, token = self.tokens[-1]
        if token_type == 'IDENTIFIER':
            self.read('IDENTIFIER', token)
            self.build_tree('IDENTIFIER', 0)
        elif token == '(':
            self.read('PUNCTUATION', '(')
            self.Vl()
            self.read('PUNCTUATION', ')')
            self.build_tree('()', 0)
        else:
            raise SyntaxError(f"Unexpected token {token}")
        
    def Vl(self):
        n = 1
        while self.tokens and self.tokens[-1][1] == ',':
            if not self.tokens:
                raise SyntaxError("Unexpected end of input")
            token_type, token = self.tokens[-1]
            if token_type == 'IDENTIFIER':
                self.read('IDENTIFIER', token)
                self.build_tree('IDENTIFIER', 0)
                while self.tokens and self.tokens[-1][1] == ',':
                    self.read('PUNCTUATION', ',')
                    self.Vl()
            else:
                raise SyntaxError(f"Unexpected token {token}")
        if n > 1:
            self.build_tree(',', n)

if __name__ == "__main__":
    scaner = Scanner()
    with open('Inputs\Q1.txt', 'r') as file:
        code = file.read()
        print("Input code:", code)
        print("Tokenized output:")
        print("========================================")
        tokens = scaner.tokenize(code)
        for i in tokens: print(i)
        print("========================================")
        tokens.reverse()
        parser = Parser(tokens)
        print("Parse tree:")
        parser.parse()
        parser.stack[0].print_tree()
    
   