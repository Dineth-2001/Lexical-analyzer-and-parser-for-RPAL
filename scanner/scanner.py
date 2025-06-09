import re
from data_structures import enums

TokenType = enums.TokenType

# Declaration of the function to tokenize and screen the code. Here we will tokenize the code and delete unwanted tokens.
def tokenize_and_screen(code):
        
    current_token = ''
    current_state = ''
    tokens = []
    valid_operators = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', 
                        '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', "'", '?']

    key_words = ['let', 'in', 'fn', 'where', 'aug', 'or', 'not', 'gr', 'ge', 'ls', 'le', 'eq',
                    'ne', 'true', 'false', 'nil', 'dummy', 'within', 'and', 'rec']

    patterns = [
        (TokenType.COMMENT, re.compile(r'//.*')),
        (TokenType.KEYWORD, re.compile(r'\b(?:' + '|'.join(key_words) + r')\b')),
        (TokenType.IDENTIFIER, re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')),
        (TokenType.INTEGER, re.compile(r'\b\d+\b')),
        (TokenType.STRING, re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')),
        (TokenType.OPERATOR, re.compile(r'->')),
        (TokenType.OPERATOR, re.compile(r'[' + re.escape(''.join(valid_operators)) + ']')),
        (TokenType.WHITESPACE, re.compile(r'[ \t\n\r]+')),
        (TokenType.PUNCTUATION, re.compile(r'[(),;]')),
        (TokenType.UNKNOWN, re.compile(r'\S+')),
    ]


    tokens = []
    i = 0

    while i < len(code):
        match = None
        for token_type, pattern in patterns:
            match = pattern.match(code, i)
            if match:
                value = match.group(0)
                if token_type == TokenType.WHITESPACE:
                    i = match.end()
                    break
                elif token_type == TokenType.STRING:
                    value = value[1:-1]
                tokens.append((token_type, value))
                i = match.end()
                break
        if not match:
            tokens.append((TokenType.UNKNOWN, code[i]))
            i += 1

    # Remove comments and whitespace tokens
    tokens = [token for token in tokens if token[0] not in (TokenType.COMMENT, TokenType.WHITESPACE)]
    
    return tokens

 
if __name__ == "__main__":
    with open('Inputs/Q5.txt', 'r') as file:
        code = file.read()

        print("Tokenized output:")
        tokens = tokenize_and_screen(code)
        for token in tokens:
            print(token)
        print("========================================")
