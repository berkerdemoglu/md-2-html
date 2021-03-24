from md_parser import Parser
from html_tag import HtmlTag, VoidHtmlTag
import webbrowser
import os
from accessify import private  # todo might remove access modifier


class MD2HTMLConverter():
	"""A class that converts markdown files to HTML5."""

	def __init__(self, filename: str, open_browser: bool = True):
		"""Initialize the converter with a file."""
		self.filename = filename
		self.html_filename = filename.replace('.md', '.html')

		self.parser = Parser(filename)

	@private
	@staticmethod
	def _generate_css():
		"""Generates CSS styling for the generated .html file."""
		css_content = ""
		# Read css from the styles file.
		with open('styles.css', 'r') as style_f:
			for line in style_f.readlines():
				css_content += line

		# Generates style tag with CSS.
		css = HtmlTag('style', attributes={'type': 'text/css'}, content=css_content)
		return css

	@private
	def _generate_head(self):
		"""Generates the head tag."""
		head = HtmlTag('head')
		# Add meta tags.
		head.add(VoidHtmlTag('meta', attributes={'content': 'text/html', 'charset': 'utf-8'}))
		head.add(VoidHtmlTag('meta', attributes={'name': 'author', 'content': 'MD2HTML'}))
		head.add(
			VoidHtmlTag('meta', attributes={'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}))
		# Add CSS and title.
		head.add(self._generate_css())

		self.parser.html.add(head)

	@private
	def _generate_body(self):
		"""Creates body and the main div."""
		body = HtmlTag('body')
		body.add(self.parser.div)

		self.parser.html.add(body)

	def convert(self):
		self._generate_head()
		self._generate_body()
		self.parser.make_tags()
		with open(self.html_filename, 'w') as f:
			f.write(str(self.parser.html))

	def __enter__(self):
		self.convert()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		os.chdir('..')
		webbrowser.open('file:///' + os.getcwd() + '/resources/document.html')
