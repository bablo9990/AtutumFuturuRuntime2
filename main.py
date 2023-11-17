import re

from kivy import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.extras.highlight import KivyLexer
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.responsivelayout import MDResponsiveLayout
from pygments.token import *
import os


class CustomLexer(KivyLexer):
    tokens = {
        'root': [
            (r'execute', Keyword),
            (r'create', Keyword),
            (r'save', Keyword),
            (r'delete', Keyword),
            (r'print', Keyword),
            (r'exit', Keyword),

            (r'file', String),
            (r'code', String),


            (r'("[^"]*")', String),
            (r"('[^']*')", String),

            (r'#.*$', Comment),

            (r'import', Operator),
            (r'from', Operator),
            (r'if', Operator),
            (r'else', Operator),
            (r'for', Operator),
            (r'while', Operator),

            (r'number', Number),
            (r'string', String),
            (r'integer', Number),
            ],
    }
def resize():
    Config.set('graphics', 'fullscreen', False)
    Config.set('graphics', 'width', 1000)
    Config.set('graphics', 'height', 600)
class MyApp(MDApp):
    def build(self):
        from kivy.config import Config

        Config.write()
        self.title = 'Future Runtime Environment'
        run = MDRaisedButton(text="", pos_hint={'top': 1}, on_release=self.compile)
        image = Image(source='run.png')
        run.add_widget(image)
        self.codeInput = CodeInput(lexer=CustomLexer(), background_color="white",)
        self.codeInput.font_name = "Menlo.ttf"
        self.OutPut = MDLabel(text="Out Put", pos_hint={'top':1}, padding=5)
        self.OutPut.font_name = "Menlo.ttf"
        layout = MDBoxLayout()

        layout.add_widget(self.codeInput)
        layout.add_widget(self.OutPut)
        layout.add_widget(run)
        return layout

    def compile(self, *args):
        self.OutPut.color = "000000"
        count = 0
        # text = self.codeInput.text.split(';')[0].replace('\n', "")
        for line in self.codeInput.text.split(';'):
            text = line.replace('\n', "")
            count += 1
            if "execute" in text:
                match = re.search(r'"([^"]*)"', text)
                if "file." in text:
                    if match:
                        filename, file_extension = os.path.splitext(match.group(1))
                        try:
                            if file_extension == ".fr":
                                print(filename+file_extension)
                                with open(filename+file_extension, 'r') as file:
                                    self.codeInput.text = file.read()
                                    if self.codeInput.text.split('\n')[0].strip().startswith("execute"):
                                        self.OutPut.text = f"Process finished with exit code 1. Warning clear unreachable code. \nRead file {filename}"
                                    else:
                                        self.OutPut.text = f"Process finished with exit code 0. \nRead file {filename}"
                            else:
                                self.OutPut.text = f"Process finished with exit code -1. \nUnsupportedCodeFormat error:" \
                                                   f" file has not compilable extension on Line {count}"
                                self.OutPut.color = "ff293a"
                                break
                        except FileNotFoundError:
                            self.OutPut.text = f"Process finished with exit code -1. \nFileNotFoundError error: file not exists on Line {count}"
                            self.OutPut.color = "ff293a"
                            break
                else:
                    self.OutPut.text = f"Process finished with exit code -1. \nNot found 'execute' method in class on Line {count}"
                    self.OutPut.color = "ff293a"
                    break
            if "save" in text:
                match = re.search(r'"([^"]*)"', text)
                filename, file_extension = os.path.splitext(match.group(1))
                if file_extension == ".fr":
                    if "file." in text:
                        with open(match.group(1), "w") as file1:
                            file1.write(self.codeInput.text)
                    else:
                        self.OutPut.text = f"Process finished with exit code -1. \nUnsupportedCodeFormat error: " \
                                           f"file has not compilable extension on Line {count}"
                        self.OutPut.color = "ff293a"
                        break
                else:
                    self.OutPut.text = f"Process finished with exit code -1. \nUnsupportedCodeFormat error:" \
                                       f" file has not compilable extension on Line {count}"
                    self.OutPut.color = "ff293a"
                    break
            if "delete" in text:
                match = re.search(r'"([^"]*)"', text)
                filename, file_extension = os.path.splitext(match.group(1))
                if file_extension == ".fr":
                    if "file." in text:
                        try:
                            os.remove(match.group(1))
                        except OSError:
                            self.OutPut.text = f"Process finished with exit code -1. \nNot found following file in directory on Line {count}"
                            self.OutPut.color = "ff293a"
                            break
                    else:
                        self.OutPut.text = f"Process finished with exit code -1. \nNot found 'delete' method in class on Line {count}"
                        self.OutPut.color = "ff293a"
                        break
                else:
                    self.OutPut.text = f"Process finished with exit code -1. \nUnsupportedCodeFormat error:" \
                                       f" file has not compilable extension on Line {count}"
                    self.OutPut.color = "ff293a"
                    break
            if "create" in text:
                arguments = re.findall(r'"([^"]*)"', text)
                if "code." in text:
                    if len(arguments) > 2:
                        if ".fr" in arguments[0]:
                            from gpt4 import Completion
                            answer = Completion().create(f"generate {arguments[2]} code by provided query and don't add any comments, write only code:"
                                                     f" "+arguments[1])
                            with open(arguments[0].replace(".fr", ".frc"), "w") as code:
                                code.write(answer)
                        else:
                            self.OutPut.text = "Process finished with exit code -1. \nUnsupportedCodeFormat error:" \
                                               f" file has not compilable extension on Line {count}"
                            self.OutPut.color = "ff293a"
                            break
                    else:
                        self.OutPut.text = f"Process finished with exit code -1. \nToo many arguments, expected " \
                                           f"2 got {len(arguments)} on Line {count}"
                        self.OutPut.color = "ff293a"
                        break
                else:
                    self.OutPut.text = f"Process finished with exit code -1. \nNot found 'execute' method in class on Line {count}"
                    self.OutPut.color = "ff293a"
                    break
            if "print" in text:
                arguments = re.search(r'"([^"]*)"', text)
                self.OutPut.text = arguments.group(1)
            if "exit" in text:
                exit(0)


if __name__ == '__main__':
    MyApp().run()
