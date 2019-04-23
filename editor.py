from tkinter import Tk, Text, Menu, filedialog, Label, Button, END, W, E, FALSE, font
from tkinter.scrolledtext import ScrolledText
from interperter import Interpreter
import subprocess
import sys


class Editor():

    def __init__(self, root):

        self.root = root
        self.file_path = None
        self.root.title('Pascal Interpreter')
        ft = font.Font(family='Consolas', size=12)

        self.program_editor_label = Label(
            root, text="Pascal Program: ", padx=10, pady=1, font=ft)

        self.program_editor_label.grid(
            sticky="W", row=0, column=0, columnspan=2, pady=3)

        self.program_editor = ScrolledText(
            root, width=100, height=25, padx=10, pady=10, font=ft)

        self.program_editor.grid(sticky=W + E, row=1,
                                 column=0, columnspan=2, padx=10)

        self.program_editor.config(wrap="word", undo=True)

        self.program_editor.focus()

        self.run_button = Button(
            root, text='Find Query result', height=2, width=20, command=self.run_query, font=ft)

        self.run_button.grid(sticky=E, row=3, column=1, pady=3, padx=10)
        self.result_label = Label(
            root, text="Query result:", padx=10, pady=1, font=ft)

        self.result_label.grid(
            sticky="W", row=4, column=0, columnspan=2, padx=10, pady=3)

        self.result_display = ScrolledText(
            root, width=100, height=10, padx=10, pady=10, font=ft)

        self.result_display.grid(
            row=5, column=0, columnspan=2, padx=10, pady=7)

        self.create_file_menu()

    def create_file_menu(self):
        self.menu_bar = Menu(root)

        file_menu = Menu(self.menu_bar, tearoff=0)

        file_menu.add_command(label="Open...", underline=1,
                              command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", underline=1,
                              command=self.save_file)
        file_menu.add_command(label="Save As...",
                              underline=5, command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Run", underline=1, command=self.run_query)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", underline=2,
                              command=self.root.destroy)

        self.menu_bar.add_cascade(label="File", underline=0, menu=file_menu)

        self.root.config(menu=self.menu_bar)

    def run_query(self):
        self.result_display.delete('1.0', END)

        self.save_file_as('_test.pas')
        p = subprocess.Popen('python spi.py _test.pas', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             shell=True, universal_newlines=True)
        output_array = []
        while True:
            line = p.stdout.readline()
            if not line:
                break
            self.result_display.insert(END, str(line))
            self.root.update()
            output_array.append(line)
        output = "".join(output_array)
        p.communicate()
        p.stdout.close()
        return output, p.returncode

    def is_file_path_selected(self, file_path):
        return file_path != None and file_path != ''

    def get_file_contents(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            file_contents = f.read()

        return file_contents

    def set_program_editor_text(self, text):
        self.program_editor.delete(1.0, "end")
        self.program_editor.insert(1.0, text)
        self.program_editor.edit_modified(False)

    def open_file(self, file_path=None):
        if file_path == None:
            file_path = filedialog.askopenfilename()

        if self.is_file_path_selected(file_path):
            file_contents = self.get_file_contents(file_path)

            self.set_program_editor_text(file_contents)
            self.file_path = file_path

    def save_file(self):
        if self.file_path == None:
            result = self.save_file_as()
        else:
            result = self.save_file_as(file_path=self.file_path)

        return result

    def write_editor_text_to_file(self, file):
        editor_text = self.program_editor.get(1.0, "end-1c")
        file.write(bytes(editor_text, 'UTF-8'))
        self.program_editor.edit_modified(False)

    def save_file_as(self, file_path=None):
        if file_path == None:
            file_path = filedialog.asksaveasfilename(
                filetypes=(
                    ('Text files', '*.txt'), ('Prolog files',
                                              '*.pl *.pro'), ('All files', '*.*')
                )
            )
        try:
            with open(file_path, 'wb') as file:
                self.write_editor_text_to_file(file)
                self.file_path = file_path
                return "saved"

        except FileNotFoundError:
            return "cancelled"

    def undo(self, event=None):
        self.program_editor.edit_undo()

    def redo(self, event=None):
        self.program_editor.edit_redo()


if __name__ == "__main__":

    root = Tk()
    editor = Editor(root)

    root.resizable(width=FALSE, height=FALSE)
    root.mainloop()
