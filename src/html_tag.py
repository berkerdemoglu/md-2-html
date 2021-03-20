from __future__ import annotations


class HtmlTag():
	single_line = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'i', 'span']
	headings = single_line[:6]

	def __init__(self, tag: str, content: str = "", child_nodes: list = None, attributes: dict = None, tab_depth: int = 0):
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

		self.tab_depth = tab_depth # Store how deep down the tree we went.

	def add(self, tag: HtmlTag):
		tag.tab_depth += self.tab_depth + 1
		print("tag.depth = " + str(tag.tab_depth))
		self.child_nodes.append(tag)

	def __str__(self):
		return repr(self)

	def __repr__(self):
		representation = (self.tab_depth * '\t') + '<' + self.tag
		# Add the attributes.
		if self.attributes:
			for attribute, value in self.attributes.items():
				representation += ' ' + attribute + '="' + value + '"'

		representation += '>'

		# Add new line and tab before adding children and content.
		if self.tag in HtmlTag.single_line:  # requires new line and tab
			representation += self.content
		else:
			representation += '\n' + self.content

		# Add children.
		for child in self.child_nodes:
			representation += ('\t' * child.tab_depth) + repr(child)

		# Close the tag.
		if self.tag in HtmlTag.single_line:
			representation += f'</{self.tag}>'
		else:
			representation += f'\n</{self.tag}>'

		if self.tag in HtmlTag.headings:
			representation += '\n'

		return representation


class VoidHtmlTag(HtmlTag):

	def __init__(self, tag: str, content, child_nodes: list = None, attributes: list = None,
				 void_element: bool = False):
		"""Initialize tag name, child tags and is void element."""
		super().__init__(tag, content, child_nodes, attributes)
		self.void_element = void_element
