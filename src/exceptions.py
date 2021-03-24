class InvalidHeadingException(Exception):
	def __init__(self):
		super().__init__("Invalid heading: more than 6 hashtags (#)")


class InvalidBoldItalicException(Exception):
	def __init__(self):
		super().__init__("Invalid heading: more than 3 asterisks (*)")