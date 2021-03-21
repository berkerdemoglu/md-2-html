from __future__ import annotations
import html5print


class HtmlTag():

	def __init__(self, tag: str, content: str = "", child_nodes: list = None, attributes: dict = None):
		"""Initialize tag name, child tags and is void element."""
		self.tag = tag
		self.content = content

		if not child_nodes:
			self.child_nodes = []
		else:
			self.child_nodes = child_nodes

		if not attributes:
			self.attributes = {}
		else:
			self.attributes = attributes

	def add(self, tag: HtmlTag):
		self.child_nodes.append(tag)

	def __str__(self):
		return repr(self)

	def __repr__(self):
		if self.tag == 'html':
			unformatted_html = '<!DOCTYPE html>'
		else:
			unformatted_html = ""

		unformatted_html += '<' + self.tag
		# Add the attributes.
		if self.attributes:
			for attribute, value in self.attributes.items():
				unformatted_html += ' ' + attribute + '="' + value + '"'

		unformatted_html += '>' + self.content

		# Add children.
		for child in self.child_nodes:
			unformatted_html += str(child)

		# Close the tag.
		unformatted_html += f'</{self.tag}>'

		representation = html5print.HTMLBeautifier.beautify(unformatted_html, indent=4)

		return representation


class VoidHtmlTag(HtmlTag):

	def __init__(self, tag: str, attributes: dict = None):
		"""Initialize tag name, child tags and is void element."""
		super().__init__(tag, attributes=attributes)

	def __str__(self):
		return repr(self)

	def __repr__(self):
		if self.tag == 'html':
			unformatted_html = '<!DOCTYPE html>'
		else:
			unformatted_html = ""

		unformatted_html += '<' + self.tag
		# Add the attributes.
		if self.attributes:
			for attribute, value in self.attributes.items():
				unformatted_html += ' ' + attribute + '="' + value + '"'

		unformatted_html += ' />'

		return unformatted_html
