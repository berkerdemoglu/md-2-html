from typing import List
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

	T_UNDERSCORE = '_'
	T_DASH = '-'
	T_LBRACKET = '['
	T_RBRACKET = ']'
	T_LPAREN = '('
	T_RPAREN = ')'
	T_EXCLAM = '!'
	T_ASTRK = '*'
	T_NEWLINE = '\n'
	T_TEXT = ""  # empty string for placeholder


class Token():
	"""A class that represents a markdown token."""

	def __init__(self, token_type: TokenType, value=None):
		self.token_type = token_type
		self.value = value

	def __repr__(self):
		return f'token_type={self.token_type}, value={str(self.value)}'

	def __str__(self):
		return f'({self.token_type})' if self.value is None else f'({self.token_type}:{self.value})'


# Lexer
class Position():
	"""A class that stores the current position being tokenized."""

	def __init__(self, idx: int, ln: int, col: int):
		self.idx = idx
		self.ln = ln
		self.col = col

	def advance(self, current_char: str) -> None:
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
			self.file_content = f.read().strip()

		self.pos = Position(-1, 0, 1)
		self.current_char = ""

		self.advance()  # so we get to the first letter

	def advance(self) -> None:
		"""Increment the position and get a new character."""
		self.pos.advance(self.current_char)
		self.current_char = self.file_content[self.pos.idx] if self.pos.idx < len(self.file_content) else ""

	def make_tokens(self) -> List[Token]:
		"""Tokenize the file and return a list of tokens."""
		while self.current_char != "":
			# TODO: to check or not to check tab character or space?
			if self.current_char == '#':
				self.tokens.append(self._make_heading())
			elif self.current_char == '-':
				self.tokens.append(Token(TokenType.T_DASH))
				self.advance()
			elif self.current_char == '[':
				self.tokens.append(Token(TokenType.T_LBRACKET))
				self.advance()
			elif self.current_char == ']':
				self.tokens.append(Token(TokenType.T_RBRACKET))
				self.advance()
			elif self.current_char == '(':
				self.tokens.append(Token(TokenType.T_LPAREN))
				self.advance()
			elif self.current_char == ')':
				self.tokens.append(Token(TokenType.T_RPAREN))
				self.advance()
			elif self.current_char == '!':
				self.tokens.append(Token(TokenType.T_EXCLAM))
				self.advance()
			elif self.current_char == '*':
				self.tokens.append(Token(TokenType.T_ASTRK))
				self.advance()
			elif self.current_char == '\n':
				self.tokens.append(Token(TokenType.T_NEWLINE))
				self.advance()
			elif self.current_char in Lexer.TEXT_CHARS:
				text_tok = self._make_text()
				if text_tok.value:
					self.tokens.append(text_tok)
			else:
				self.advance()

		return self.tokens

	def _make_heading(self) -> Token:
		"""Returns a heading token (h1, h2 etc.)."""
		hash_tag_count = 0  # keeps track of hash tags.
		while self.current_char == '#' and hash_tag_count != 6:
			hash_tag_count += 1
			self.advance()
		token_type = TokenType['T_H' + str(hash_tag_count)]  # determine heading tag

		heading_text = ""
		while self.current_char != '\n':  # while still parsing the same line as the heading
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
