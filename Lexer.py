import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = self.tokenize()
        self.index = 0  # Keeps track of the current token
    
    def tokenize(self):
        patterns = {
            'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'INT': r'\d+',
            'STRING': r'\".*?\"',
            'SYMBOL': r'[=+->,|&*(){};]',
            'KEYWORD': r'\b(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|rec|true|false|nil|dummy|and|within)\b',
            'WHITESPACE': r'\s+'
        }
        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns.items())
        tokens = []
        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup
            value = match.group(kind)
            if kind != 'WHITESPACE':
                tokens.append((kind, value))
        return tokens
    
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
