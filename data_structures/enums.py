from enum import Enum

class TokenType(Enum):
    COMMENT = '<COMMENT>'
    KEYWORD = '<KEYWORD>'
    IDENTIFIER = '<IDENTIFIER>'
    INTEGER = '<INTEGER>'
    STRING = '<STRING>'
    OPERATOR = '<OPERATOR>'
    WHITESPACE = '<WHITESPACE>'
    PUNCTUATION = '<PUNCTUATION>'
    UNKNOWN = '<UNKNOWN>'
