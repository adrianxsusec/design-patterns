import tkinter
from tkinter import Tk, ttk, Canvas, Frame
from tkinter.font import Font


class TryoutComponent(Canvas):
    def __init__(self, master):
        super().__init__(master, width=300, height=200)
        self.master = master
        self.pack()

        self.create_line(0, 100, 300, 100, fill="red")
        self.create_line(150, 0, 150, 200, fill="red")

        self.create_text(150, 50, text="First line")
        self.create_text(150, 150, text="Second line")

        self.bind("<Return>", self.close_window)

        self.focus_set()

    def close_window(self, event):
        self.master.destroy()


class TextEditor(Canvas):
    def __init__(self, master, model):
        super().__init__(master, width=400, height=300)
        self.model: TextEditorModel = model
        self.font = Font(family="Courier", size=18)
        self.line_height = 20
        self.char_width = self.font.measure('m')
        self.left_padding = 5

        self.bind('<Key>', self.on_key)
        # self.bind('<Button-1>', self.on_click)
        self.focus_set()

    def on_key(self, event: tkinter.Event):
        if event.keysym == 'Return':
            self.insert_newline()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Left':
            self.move_cursor(-1, 0)
        elif event.keysym == 'Right':
            self.move_cursor(1, 0)
        elif event.keysym == 'Up':
            self.move_cursor(0, -1)
        elif event.keysym == 'Down':
            self.move_cursor(0, 1)
        elif len(event.char) == 1:
            self.insert_char(event.char)
        self.redraw()

    def redraw(self):
        self.delete('all')

        for ind, line in enumerate(self.model.lines):
            self.create_text(self.left_padding, ind * self.line_height, anchor='nw', text=line, font=self.font)

        cursor_x = self.left_padding + self.model.cursor_location.column * self.char_width
        cursor_y = self.model.cursor_location.row * self.line_height
        self.create_line(cursor_x, cursor_y, cursor_x, cursor_y + self.line_height, fill='red')

    def insert_newline(self):
        row = self.model.cursor_location.row
        column = self.model.cursor_location.column

        current_line = self.model.lines[row]
        self.model.lines[row] = current_line[:column]
        self.model.lines.insert(row + 1, current_line[column:])

        self.model.cursor_location.column = 0
        self.model.cursor_location.row += 1

    def backspace(self):
        row = self.model.cursor_location.row
        column = self.model.cursor_location.column

        if column > 0:
            self.model.lines[row] = self.model.lines[row][:column - 1] + self.model.lines[row][column:]
            self.model.cursor_location.column -= 1

        elif row > 0:
            self.model.cursor_location.column = len(self.model.lines[row - 1])
            self.model.cursor_location.row -= 1
            self.model.lines[row - 1] += self.model.lines[row]
            del self.model.lines[row]

    def insert_char(self, char):
        row = self.model.cursor_location.row
        column = self.model.cursor_location.column

        self.model.lines[row] = self.model.lines[row][:column] + char + self.model.lines[row][column:]
        self.model.cursor_location.column += 1

    def move_cursor(self, dx, dy):
        new_row = self.model.cursor_location.row + dy
        new_col = self.model.cursor_location.column + dx

        # Ensure we don't go out of bounds vertically
        new_row = max(0, min(new_row, len(self.model.lines) - 1))

        # Handle moving left at the beginning of a line
        if dx < 0 and new_col < 0 and new_row > 0:
            new_row -= 1
            new_col = len(self.model.lines[new_row])
        # Handle moving right at the end of a line
        elif dx > 0 and new_col > len(self.model.lines[new_row]) and new_row < len(self.model.lines) - 1:
            new_row += 1
            new_col = 0
        else:
            # Ensure we don't go out of bounds horizontally
            new_col = max(0, min(new_col, len(self.model.lines[new_row])))

        self.model.cursor_location = Location(new_row, new_col)


class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class LocationRange:
    def __init__(self, start_location: Location, end_location: Location):
        self.start_location = start_location
        self.end_location = end_location


class TextEditorModel:
    def __init__(self, text=""):
        self.lines: list = text.split('\n')
        self.selection_range = None
        self.cursor_location: Location = Location(0, 0)


def main1():
    root = Tk()
    component = TryoutComponent(root)
    root.mainloop()


def test_text_editor_model():
    text = "First line.\nSecond line.\nThird line."
    tem = TextEditorModel(text)
    [print(line) for line in tem.lines]
    print()


def test_text_editor():
    root = Tk()

    text = "First line.\nSecond line.\nThird line."
    model = TextEditorModel(text)
    editor = TextEditor(master=root, model=model)

    editor.pack()
    editor.redraw()
    root.mainloop()


if __name__ == "__main__":
    test_text_editor()
