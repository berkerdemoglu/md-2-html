from typing import List, Tuple, NoReturn

from md_2_html.lexer._token import Token, TokenType

__all__ = [
    "Lexer"
]

# Lexer
class Position():
    """A class that stores the current position being tokenized."""

    def __init__(self, idx: int, ln: int, col: int):
        """Initialize the character index, line and column number."""
        self.idx = idx
        self.ln = ln
        self.col = col

    def advance(self, current_char: str) -> NoReturn:
        """Increment the position."""
        self.idx += 1
        self.col += 1

        if current_char != '\n':
            self.ln += 1
            self.col = 0


class Lexer():
    """A class that creates tokens from a .md file."""
    LETTERS = 'abcdefghijklmnopqrstuvxyz'
    DIGITS = '0123456789'
    NON_TOKENS = "\" :/.?=\t"  # todo check again
    TEXT_CHARS = LETTERS + LETTERS.upper() + DIGITS + NON_TOKENS  # Store all non token characters in a class variable

    def __init__(self, filename: str):
        """Initialize an empty list of tokens, read the file content and position."""
        self.tokens = []

        with open(filename, 'r') as f:
            self.file_content = f.read().rstrip() + "\n"  # read the file add a new line to avoid errors in lexing

        # Initialize position to be tokenized and a flag for checking new line.
        self.pos = Position(-1, 0, 1)
        self.current_char = ""
        self.not_newline = True

        self.advance()  # so we get to the first letter

    def advance(self) -> NoReturn:
        """Increment the position and get a new character."""
        self.pos.advance(self.current_char)
        self.current_char = self.file_content[self.pos.idx] if self.pos.idx < len(self.file_content) else ""
        self.not_newline = self.current_char != '\n'

    def make_tokens(self) -> List[Token]:
        """Tokenize the file and return a list of tokens."""
        while self.current_char != "":
            # TODO: to check or not to check tab character or space?
            if self.current_char == '#':
                self.tokens.append(self._make_heading())
            elif self.current_char == '*':
                self.tokens.append(Token(TokenType.T_ASTRK))
                self.advance()
            elif self.current_char == '[':
                link_text, url = self._make_link()
                self.tokens.append(link_text)
                self.tokens.append(url)
            elif self.current_char == '!':
                alt_text, image_link = self._make_image()
                self.tokens.append(alt_text)
                self.tokens.append(image_link)
                self.advance()
            elif self.current_char == '`':
                self.tokens.append(self._make_code())
            elif self.current_char == '-':
                self.tokens.append(self._make_hr())
            elif self.current_char in Lexer.TEXT_CHARS:
                text_tok = self._make_text()
                if text_tok.value:
                    self.tokens.append(text_tok)
            else:
                self.advance()

        return self.tokens

    def _make_hr(self) -> Token:
        """Returns a horizontal rule token if there are 3 or more dashes and the line ends, else, returns a text token."""
        dash_count = 0
        while self.current_char == '-' and self.not_newline:  # while still reading dashes
            dash_count += 1
            self.advance()

        if dash_count >= 3:
            return Token(TokenType.T_HR)

    def _make_code(self) -> Token:
        """Returns a code token, TODO: returns inline code token at the moment."""
        code = ""  # empty string to store code
        self.advance()  # skip ` character
        while self.current_char != '`':  # while still reading code
            code += self.current_char
            self.advance()

        self.advance()  # skip ` character again

        return Token(TokenType.T_INLINE_CODE, code)

    def _make_heading(self) -> Token:
        """Returns a heading token"""
        hash_tag_count = 0  # keeps track of hash tags.
        while self.current_char == '#' and hash_tag_count != 6:
            hash_tag_count += 1
            self.advance()
        token_type = TokenType['T_H' + str(hash_tag_count)]  # determine heading tag

        heading_text = ""
        while self.current_char and self.not_newline:  # while still parsing the same line as the heading
            heading_text += self.current_char
            self.advance()

        return Token(token_type, heading_text.strip())  # strip unnecessary spaces

    def _make_text(self) -> Token:
        """Returns a text token with the value of the token being the content of the text."""
        text = ""  # Create an empty string to store characters
        while self.current_char in Lexer.TEXT_CHARS:
            text += self.current_char
            self.advance()

        return Token(TokenType.T_TEXT, text.strip())

    def _make_link(self) -> Tuple[Token, Token]:
        """Returns two tokens, one consisting of the link text and one consisting of the URL."""
        # Read the link text.
        link_text = ""
        self.advance()  # skip [ character
        while self.current_char != ']' and self.not_newline:
            link_text += self.current_char
            self.advance()

        # Skip ] and ( characters.
        if self.current_char == ']':
            self.advance()

        if self.current_char == '(':
            self.advance()

        # Read the URL.
        url = ""
        while self.current_char != ')' and self.not_newline:
            url += self.current_char
            self.advance()

        return Token(TokenType.T_LINKTEXT, link_text), Token(TokenType.T_HREF, url)

    def _make_image(self) -> Tuple[Token, Token]:
        # Read the link text.
        alt_text = ""
        # Skip ! and [ characters.
        self.advance()
        if self.current_char == '[':
            self.advance()

        while self.current_char != ']' and self.not_newline:
            alt_text += self.current_char
            self.advance()

        # Skip ] and ( characters.
        if self.current_char == ']':
            self.advance()

        if self.current_char == '(':
            self.advance()

        # Read the URL.
        image_link = ""
        while self.current_char != ')' and self.not_newline:
            image_link += self.current_char
            self.advance()

        return Token(TokenType.T_IMG_ALTTEXT, alt_text), Token(TokenType.T_SRC, image_link)
