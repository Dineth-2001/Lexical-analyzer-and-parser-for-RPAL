import re

class Scanner:
    def __init__(self):
        self.current_token = ''
        self.current_state = ''
        self.tokens = []

        self.valid_operators = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', 
                                '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', "'", '?']
        
        self.key_words = ['let', 'in', 'fn', 'where', 'aug', 'or', 'not', 'gr', 'ge', 'ls', 'le', 'eq',
                          'ne', 'true', 'false', 'nil', 'dummy', 'within', 'and', 'rec']

        self.patterns = [
            ('COMMENT', re.compile(r'//.*')),
            ('KEYWORD', re.compile(r'\b(?:' + '|'.join(self.key_words) + r')\b')),
            ('IDENTIFIER', re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')),
            ('INTEGER', re.compile(r'\b\d+\b')),
            ('STRING', re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')),
            ('OPERATOR', re.compile(r'[' + re.escape(''.join(self.valid_operators)) + r']+')),
            ('WHITESPACE', re.compile(r'[ \t\n\r]+')),
            ('PUNCTUATION', re.compile(r'[(),;]')),
            ('UNKNOWN', re.compile(r'\S+')),
        ]

    def tokenize(self, code):
        self.tokens = []
        i = 0

        while i < len(code):
            match = None
            for token_type, pattern in self.patterns:
                match = pattern.match(code, i)
                if match:
                    value = match.group(0)
                    if token_type == 'WHITESPACE':
                        i = match.end()
                        break
                    elif token_type == 'STRING':
                        value = value[1:-1]
                    self.tokens.append((token_type, value))
                    i = match.end()
                    break
            if not match:
                self.tokens.append(('UNKNOWN', code[i]))
                i += 1

        return self.tokens
    
    

if __name__ == "__main__":
    scanner = Scanner()
    with open('Inputs\Q1.txt', 'r') as file:
        code = file.read()
        print("Input code:", code)
        print("Tokenized output:")
        print("========================================")
        tokens = scanner.tokenize(code)
        for token in tokens:
            print(token)
