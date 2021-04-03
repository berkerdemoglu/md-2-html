import os

from tkinter import *
from tkinter import filedialog

from converter import MD2HTMLConverter

FONT = ('Segoe UI', 13)
BG_COLOR = "#282c34"
FG_COLOR = "#abb2bf"


class GUIApp():
	"""A class that allows the user to select a markdown file to convert."""

	def __init__(self):
		"""Initialize the app with a root."""
		# Initialize root and its attributes.
		self.root = Tk()
		self.root.title('md-2-html')
		self.root.iconbitmap('../assets/icon.ico')
		self.root.geometry('720x540')  # 4:3 ratio
		self.root.configure(bg=BG_COLOR)
		self.root.resizable(False, False)

		# Make a heading label.
		self.heading_label = Label(self.root, text='md-2-html', font=('Segoe UI', 24), bg=BG_COLOR, fg=FG_COLOR)

		# Make a frame for the converter.
		self.converter_frame = LabelFrame(self.root, text='Convert Markdown to HTML', padx=10, pady=10,
										  font=FONT, bg=BG_COLOR, fg=FG_COLOR)

		# Make a button that opens the file selecting menu and a label that shows the file selected.
		self.file_button = Button(self.converter_frame, text='Select File', padx=5, pady=5, command=self.choose_file_cmd,
				font=FONT, bg=BG_COLOR, fg=FG_COLOR)
		self.selected_file_label = Label(self.converter_frame, text='Selected File: None', font=FONT, bg=BG_COLOR, fg=FG_COLOR)

		# Make a convert button.
		self.convert_button = Button(self.converter_frame, text='Convert', padx=5, pady=5, state='disabled',
			command=self.convert_cmd, font=FONT, bg=BG_COLOR, fg=FG_COLOR)

		# Make a radio button frame for options.
		self.options_frame = LabelFrame(self.root, text='Options', padx=10, pady=10, font=FONT, bg=BG_COLOR,
										fg=FG_COLOR)

		# Make string variables and radio buttons and a button that resets options.
		self.open_browser = BooleanVar()

		self.open_browser_radiobutton = Radiobutton(self.options_frame, text='Open in web browser when done',
				variable=self.open_browser, value=True, padx=5, pady=5, font=FONT, bg=BG_COLOR, fg=FG_COLOR)

		self.reset_options_button = Button(self.options_frame, text='Reset Options', command=self.reset_options,
				font=FONT, bg=BG_COLOR, fg=FG_COLOR)

	def draw(self):
		"""Put all widgets on the screen."""
		# Heading widget
		self.heading_label.pack(anchor='center')

		# Converter frame widgets
		self.converter_frame.pack(anchor='center', padx=20, pady=20)
		self.file_button.pack(anchor='center')
		self.selected_file_label.pack(anchor='center')
		self.convert_button.pack(anchor='center')

		# Options frame widgets
		self.options_frame.pack(anchor='center', padx=20, pady=20)
		self.open_browser_radiobutton.grid(row=0, column=0)
		self.reset_options_button.grid(row=1, column=0, columnspan=2)

	def start_app(self):
		"""Draw all widgets and start the main loop."""
		self.draw()
		self.root.mainloop()

	# COMMANDS
	def choose_file_cmd(self):
		"""Open a file dialog that allows the user to select a file to convert."""
		# Open file dialog.
		self.root.filename = filedialog.askopenfilename(initialdir=os.path.join(os.environ['USERPROFILE'], 'Desktop'),
				title='Select a Markdown File', filetypes=(('Markdown Files', '*.md'), ('All Files', '*.*')))

		# Update labels.
		self.selected_file_label['text'] = f'Selected File: {os.path.basename(self.root.filename)}'
		self.convert_button['state'] = 'normal'

	def convert_cmd(self):
		"""Convert the selected Markdown file to a HTML file."""
		open_browser = True if self.open_browser else False

		with MD2HTMLConverter(self.root.filename, open_browser) as converter:
			print(converter.parser.html)

	def reset_options(self):
		"""Deselect all radio buttons in the options frame."""
		self.open_browser_radiobutton.deselect()
