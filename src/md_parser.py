from html_tag import HtmlTag, VoidHtmlTag
import exceptions as err


class Parser():
	"""A class that both parses and lexes the markdown file."""

	def __init__(self, filename: str):
		"""Read the file content and initialize position and <html> tag."""
		with open(filename, 'r') as f:
			self.lines = f.readlines()

		# Create the html and the main div tag.
		self.html = HtmlTag('html', attributes={'lang': 'en-CA'})
		self.div = HtmlTag('div', attributes={'class': 'main container'})

		self.line = None
		self.pos = -1
		self.current_char = None

	def advance(self):
		"""Increment the character position by 1."""
		self.pos += 1
		self.current_char = self.line[self.pos] if self.pos < len(self.line) else None

	def make_tags(self):
		"""Make html tags."""
		for line in self.lines:
			self.line = line.replace('\n', '')
			self.pos = -1
			self.current_char = None
			self.advance()
			self.make_tag()

	def make_tag(self):
		"""Make tag from one line"""
		while self.current_char is not None:
			if self.current_char == '#':
				self.div.add(self.make_heading())
			elif self.current_char == '*':
				self.div.add(self.make_bold_italic())
			elif self.current_char == '[':
				self.div.add(self.make_link())
			elif self.current_char == '!':
				self.div.add(self.make_image())
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
		if content[0] == ' ': # Remove unnecessary space if it exists
			content = content[1:len(content) - 1]

		content = content.replace('\n', '')

		return HtmlTag(tag, content, attributes={'class': tag})  # class='h1' for example

	def make_bold_italic(self):
		"""Make either a bold tag, italic tag or both"""

		left_star_count = 0  # Keep track of asterisks
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

		# Remove first blank space if it exists.
		content = content[1:] if content[0] == ' ' else content

		if left_star_count == right_star_count:
			if left_star_count == 1:  # italic
				return HtmlTag('i', content)
			elif left_star_count == 2:  # bold
				return HtmlTag('b', content)
			else:  # if bold and italic, wrap bold tag in italic tag
				italic = HtmlTag('i', str(HtmlTag('b', content)))
				return italic
		elif left_star_count > right_star_count:  # add asterisks to the left
			star_difference = left_star_count - right_star_count
			content = (star_difference * '*') + content
			if right_star_count % 2 == 0:  # if bold
				return HtmlTag('b', content)
			else:  # if italic
				return HtmlTag('i', content)

		else:  # add asterisks to the right
			star_difference = right_star_count - left_star_count
			content = (star_difference * '*') + content
			if right_star_count % 2 == 0:  # if bold
				return HtmlTag('b', content)
			else:  # if italic
				return HtmlTag('i', content)

	def make_link(self):
		"""Makes a link, <a> tag."""
		link_text = ""  # create an empty string to store the link text
		self.advance()
		while self.current_char != ']':  # while parsing link text
			link_text += self.current_char
			self.advance()

		self.advance()

		ref_link = ""  # create an empty string to store the link
		if self.current_char == '(':  # a link is about to be parsed
			self.advance()
			while self.current_char != ')':
				ref_link += self.current_char
				self.advance()

		return HtmlTag('a', link_text, attributes={'href': ref_link})

	def make_image(self):
		"""Makes an image, <img> tag."""
		alt_text = ""  # create an empty string to store the link text
		self.advance()
		self.advance()
		while self.current_char != ']':  # while parsing link text
			alt_text += self.current_char
			self.advance()

		self.advance()

		img_link = ""  # create an empty string to store the link
		if self.current_char == '(':  # a link is about to be parsed
			self.advance()
			while self.current_char != ')':
				img_link += self.current_char
				self.advance()

		return VoidHtmlTag('img', attributes={'alt': alt_text, 'src': img_link})
