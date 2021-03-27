from html_tag import HtmlTag, VoidHtmlTag
from lexer import Lexer


class Parser():
	"""Parses the tokens coming from the lexer."""

	def __init__(self, filename: str):
		"""Initialize the <html> tag and lexer."""
		self.html = HtmlTag('html', attributes={'lang': 'en-CA', 'class': 'html'})
		self.div = HtmlTag('div', attributes={'class': 'main container'})

		self.lexer = Lexer(filename)
		self.tokens = self.lexer.make_tokens()

	def parse(self):
		# todo, not implemented yet
		for token in self.tokens:
			print(str(token))
