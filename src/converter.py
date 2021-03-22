from md_parser import Parser
from html_tag import HtmlTag, VoidHtmlTag
import webbrowser
import os


class MD2HTMLConverter():

	def __init__(self, filename: str):
		self.filename = filename
		self.html_filename = filename.replace('.md', '.html')

		self.parser = Parser(filename)

	@staticmethod
	def _generate_css():
		css_content = """
            html {
                font-family: \"Segoe UI\";
            }
            
            .main {
                width: 838px;
                margin: auto;
                border: 1px solid #e1e4e8;
                padding: 15px;
                padding-top: 10px;
            }
        """

		css = HtmlTag('style', attributes={'type': 'text/css'}, content=css_content)

		return css

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

	def __exit__(self, exc_type, exc_val, exc_tb):
		os.chdir('..')
		webbrowser.open('file:///' + os.getcwd() + '/resources/document.html')
