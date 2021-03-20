from __future__ import annotations

class HtmlTag():
	single_line = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'i', 'span']

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
		representation = "<" + self.tag

		# Add attributes if any.
		if self.attributes:
			for attribute, value in self.attributes.items():
				representation += " " + attribute + "=\"" + value + "\""

		representation += ">"

		# Add content.
		if self.tag in HtmlTag.single_line:
			representation += self.content
		else:
			representation += "\n\t\t" + self.content

		# Add children if any.
		if self.child_nodes:
			for child in self.child_nodes:
				representation += "\n\t" + repr(child)

		# Close the tag.
		if self.tag in HtmlTag.single_line:
			representation += f'\t</{self.tag}>'
		else:
			representation += f'\n</{self.tag}>'

		return representation



class VoidHtmlTag(HtmlTag):

	def __init__(self, tag: str, content, child_nodes: list = None, attributes: list=None, void_element: bool=False):
		"""Initialize tag name, child tags and is void element."""
		super().__init__(tag, content, child_nodes, attributes)
		self.void_element = void_element