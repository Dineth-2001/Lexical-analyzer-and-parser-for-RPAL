class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def advance(self):
        self.index += 1

    def match(self, expected_type):
        token = self.peek()
        if token and token[0] == expected_type:
            self.advance()
            return token
        return None

    def parse(self):
        return self.expression()

    # Expression Grammar Rule (E -> 'let' D 'in' E | 'fn' Vb+ '.' E | Ew)
    def expression(self):
        if self.match("KEYWORD") and self.tokens[self.index - 1][1] == "let":
            return ("let", self.definition(), self.expression())
        elif self.match("KEYWORD") and self.tokens[self.index - 1][1] == "fn":
            variables = []
            while self.peek() and self.peek()[0] == "ID":
                variables.append(self.match("ID")[1])
            self.match("SYMBOL")  # Match '.'
            return ("lambda", variables, self.expression())
        else:
            return self.ew()

    # Ew -> T 'where' Dr | T
    def ew(self):
        left = self.tuple_expression()
        if self.match("KEYWORD") and self.tokens[self.index - 1][1] == "where":
            return ("where", left, self.definition_rule())
        return left

    # T -> Ta(',' Ta )+ | Ta
    def tuple_expression(self):
        left = self.tuple_concat()
        if self.match("SYMBOL") and self.tokens[self.index - 1][1] == ",":
            elements = [left]
            while self.match("SYMBOL") and self.tokens[self.index - 1][1] == ",":
                elements.append(self.tuple_concat())
            return ("tau", elements)
        return left

    # Dr -> 'rec' Db | Db
    def definition_rule(self):
        if self.match("KEYWORD") and self.tokens[self.index - 1][1] == "rec":
            return ("rec", self.definition_body())
        return self.definition_body()

    # Db -> Vl '=' E | '(' D ')'
    def definition_body(self):
        if self.match("SYMBOL") and self.tokens[self.index - 1][1] == "(":
            definition = self.definition()
            self.match("SYMBOL")  # Match ')'
            return definition
        variable_list = self.variable_list()
        self.match("SYMBOL")  # Match '='
        return ("=", variable_list, self.expression())

    # Vl -> '<IDENTIFIER>' list ','
    def variable_list(self):
        variables = []
        while self.match("ID"):
            variables.append(self.tokens[self.index - 1][1])
            if not self.match("SYMBOL") or self.tokens[self.index - 1][1] != ",":
                break
        return variables

    # Definitions (D -> Da 'within' D | Da)
    def definition(self):
        left = self.definition_and()
        if self.match("KEYWORD") and self.tokens[self.index - 1][1] == "within":
            return ("within", left, self.definition())
        return left

    # Da -> Dr ('and' Dr)+ | Dr
    def definition_and(self):
        left = self.definition_rule()
        if self.match("KEYWORD") and self.tokens[self.index - 1][1] == "and":
            definitions = [left]
            while self.match("KEYWORD") and self.tokens[self.index - 1][1] == "and":
                definitions.append(self.definition_rule())
            return ("and", definitions)
        return left
