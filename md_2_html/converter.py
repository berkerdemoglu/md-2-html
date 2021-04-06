from md_2_html.md_parser import Parser
from md_2_html.html_tag import HtmlTag, VoidHtmlTag
from md_2_html import resources_path
import webbrowser
import os

from typing import NoReturn, Tuple


class MD2HTMLConverter():
	"""A class that converts markdown files to HTML5."""

	def __init__(self, filename: str, open_browser: bool = True):
		"""Initialize the converter with a file."""
		self.filename = filename
		self.html_filename = filename.replace('.md', '.html')

		self.open_browser = open_browser

		self.parser = Parser(filename)

	@staticmethod
	def _generate_css() -> Tuple[VoidHtmlTag, VoidHtmlTag]:
		"""Generates CSS styling for the generated .html file."""
		bootstrap = "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
		css_bootstrap = VoidHtmlTag('link', attributes={'rel': 'stylesheet', 'href': bootstrap})
		styles = "https://raw.githubusercontent.com/berkerdemoglu/md-2-html/master/assets/styles.css"
		css_styles = VoidHtmlTag('link', attributes={'rel': 'stylesheet', 'href': styles})

		return css_bootstrap, css_styles

	def _generate_head(self) -> NoReturn:
		"""Generates the head tag."""
		head = HtmlTag('head')
		# Add meta tags.
		head.add(VoidHtmlTag('meta', attributes={'content': 'text/html', 'charset': 'utf-8'}))
		head.add(VoidHtmlTag('meta', attributes={'name': 'author', 'content': 'MD2HTML'}))
		head.add(
			VoidHtmlTag('meta', attributes={'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}))
		# Add CSS and title.
		style_tags = self._generate_css()
		head.add(style_tags[0])
		head.add(style_tags[1])

		self.parser.html.add(head)

	def _generate_body(self) -> NoReturn:
		"""Creates body and the main div."""
		body = HtmlTag('body')
		body.add(self.parser.div)

		self.parser.html.add(body)

	def convert(self) -> NoReturn:
		"""Parses markdown and outputs in the form of an .html file."""
		self._generate_head()
		self._generate_body()
		self.parser.parse()
		with open(self.html_filename, 'w') as f:
			f.write(str(self.parser.html))

	# Context Manager Magic Methods
	def __enter__(self):
		self.convert()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.open_browser:
			webbrowser.open(resources_path.as_uri() + '/document.html')
