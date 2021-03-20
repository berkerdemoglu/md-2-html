from html_tag import HtmlTag, VoidHtmlTag
import exceptions as err

class Parser():
	"""A class that both parses and lexes the markdown file."""

	def __init__(self, filename):
		"""Read the file content and initialize position and <html> tag."""
		with open(filename, 'r') as f:
			self.lines = f.readlines()

		self.html = HtmlTag('html')

		self.line = None
		self.pos = -1
		self.current_char = None

	### LEXER ###
	def advance(self):
		"""Increment the character position by 1."""
		self.pos += 1
		self.current_char = self.line[self.pos] if self.pos < len(self.line) else None

	def make_tags(self):
		"""Make html tags."""
		for line in self.lines:
			self.line = line
			self.pos = -1
			self.current_char = None
			self.advance()
			self.make_tag()


	def make_tag(self):
		"""Make tag from one line."""
		while self.current_char != None:
			if self.current_char == '#': # If header
				self.html.add(self.make_heading())
			elif self.current_char == '*':
				p_tag = HtmlTag('p')
				p_tag.add(self.make_bold_italic())
				self.html.add(p_tag)
			else:
				self.advance()

	def make_heading(self) -> HtmlTag:
		"""Make a heading tag e.g <h1>"""
		hash_count = 0 # Keep track of hashtags

		while self.current_char is not None and hash_count <= 6:
			if self.current_char == '#':
				hash_count += 1
				if hash_count > 6: # if there are hashtags more than 6
					raise err.InvalidHeadingException
			else:
				break
			self.advance()

		content = ""  # Store the content of the heading tag
		while self.current_char is not None:
			content += self.current_char
			self.advance()

		tag = 'h' + str(hash_count)
		return HtmlTag(tag, content)

	def make_bold_italic(self):
		"""Make either a bold tag, italic tag or both. todo add non-tag asterisks"""
		left_non_content = "" # asterisks to the left that don't belong in the tag
		right_non_content = "" # asterisks to the right that don't belong in the tag

		left_star_count = 0 # Keep track of asterisks
		content = ""  # Store the content of the bold/italic text
		while self.current_char is not None and self.current_char == '*':
			left_star_count += 1
			self.advance()

		while self.current_char is not None and self.current_char != '*': # while still parsing text
			content += self.current_char
			self.advance()

		right_star_count = 0
		while self.current_char is not None and self.current_char == '*': # while the asterisks on both sides still match
			right_star_count += 1
			self.advance()

		if left_star_count == right_star_count:
			if left_star_count == 1: # italic
				return HtmlTag('i', content)
			elif left_star_count == 2: # bold
				return HtmlTag('b', content)
			else:
				if left_star_count % 2 == 0: # if bold bold e.g 4 asterisks
					return HtmlTag('b', content)
				else: # if bold-italic
					italic = HtmlTag('i')
					italic.add(HtmlTag('b', content))
					return italic
		else:
			return HtmlTag('lol')
