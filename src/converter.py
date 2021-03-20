from md_parser import Parser
import webbrowser
import os

class MD2HTMLConverter():

    def __init__(self, filename: str):
        self.filename = filename
        self.html_filename = filename.replace('.md', '.html')

        self.parser = Parser(filename)

    def convert(self):
        self.parser.make_tags()
        with open('../out/' + self.html_filename, 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write(str(self.parser.html))

        print(self.parser.html)

        # os.chdir('..')
        # webbrowser.open('file:///' + os.getcwd() + '/resources/document.html')
