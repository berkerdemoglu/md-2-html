from typing import List, Tuple
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

	T_TEXT = 'T_TEXT'  # token type for any type of string

	T_LINKTEXT = 'T_LINKTEXT'  # token type for text inside a link
	T_HREF = 'T_HREF'  # token type for href attribute of a link

	T_IMG_ALTTEXT = 'T_IMG_ALTTEXT'  # token type for alt attribute of an image
	T_SRC = 'T_SRC'  # token type for source for src attribute of an image

	# All other token types.
	T_UNDERSCORE = '_'
	T_DASH = '-'
	T_EXCLAM = '!'
	T_ASTRK = '*'
	T_NEWLINE = '\n'


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
		"""Initialize the character index, line and column number."""
		self.idx = idx
		self.ln = ln
		self.col = col

	def advance(self, current_char: str) -> None:
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
				link_text, url = self._make_link()
				self.tokens.append(link_text)
				self.tokens.append(url)
			elif self.current_char == '!':
				alt_text, image_link = self._make_image()
				self.tokens.append(alt_text)
				self.tokens.append(image_link)
				self.advance()
			elif self.current_char == '*':
				self.tokens.append(Token(TokenType.T_ASTRK))
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

	def _make_link(self) -> Tuple[Token, Token]:
		"""Returns two tokens, one consisting of the link text and one consisting of the URL."""
		# Read the link text.
		link_text = ""
		self.advance()  # skip [ character
		while self.current_char != ']':
			link_text += self.current_char
			self.advance()

		# Skip [ and ) characters.
		self.advance()
		self.advance()

		# Read the URL.
		url = ""
		while self.current_char != ')':
			url += self.current_char
			self.advance()

		return Token(TokenType.T_LINKTEXT, link_text), Token(TokenType.T_HREF, url)

	def _make_image(self) -> Tuple[Token, Token]:
		# Read the link text.
		alt_text = ""
		# Skip ! and [ characters.
		self.advance()
		self.advance()
		while self.current_char != ']':
			alt_text += self.current_char
			self.advance()

		# Skip [ and ) characters.
		self.advance()
		self.advance()

		# Read the URL.
		image_link = ""
		while self.current_char != ')':
			image_link += self.current_char
			self.advance()

		return Token(TokenType.T_IMG_ALTTEXT, alt_text), Token(TokenType.T_SRC, image_link)
