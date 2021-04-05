from enum import Enum

# TOKENS
class TokenType(Enum):
    """A class that has variables that distinguish a token type."""
    # Heading Tokens
    T_H1 = 'T_H1'
    T_H2 = 'T_H2'
    T_H3 = 'T_H3'
    T_H4 = 'T_H4'
    T_H5 = 'T_H5'
    T_H6 = 'T_H6'

    T_TEXT = 'T_TEXT'  # for any type of string

    T_LINKTEXT = 'T_LINKTEXT'  # for text inside a link
    T_HREF = 'T_HREF'  # for href attribute of a link

    T_IMG_ALTTEXT = 'T_IMG_ALTTEXT'  # for alt attribute of an image
    T_SRC = 'T_SRC'  # for source for src attribute of an image

    T_INLINE_CODE = 'T_INLINE_CODE'  # for inline code like `foo`

    T_HR = 'T_HR'  # for horizontal rule

    # All other token types.
    T_UNDERSCORE = '_'
    T_EXCLAM = '!'
    T_ASTRK = '*'
    T_NEWLINE = '\n'


class Token():
    """A class that represents a markdown token."""

    def __init__(self, token_type: TokenType, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f'token_type={self.token_type.name}, value={str(self.value)}'

    def __str__(self):
        return f'({self.token_type.name})' if self.value is None else f'({self.token_type.name}:{self.value})'