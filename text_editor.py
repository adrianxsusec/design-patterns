import tkinter
from abc import ABC, abstractmethod
from tkinter import Tk, ttk, Canvas, Frame
from tkinter.font import Font


class CursorObserver(ABC):
    @abstractmethod
    def update_cursor_location(self, loc):
        pass


class TextObserver(ABC):
    @abstractmethod
    def update_text(self):
        pass


class TextEditor(Canvas, CursorObserver, TextObserver):
    def __init__(self, master, model):
        super().__init__(master, width=400, height=300)
        self.model: TextEditorModel = model
        self.font = Font(family="Courier", size=18)
        self.line_height = 20
        self.char_width = self.font.measure('m')
        self.left_padding = 5

        self.cursor = None

        self.model.add_cursor_observer(self)
        self.model.add_text_observer(self)

        self.bind('<Key>', self.on_key)
        # self.bind('<Button-1>', self.on_click)
        self.focus_set()

    def on_key(self, event: tkinter.Event):
        if event.keysym == 'Return':
            self.model.insert_newline()
        elif event.keysym == 'BackSpace':
            self.model.delete_before()
        elif event.keysym == 'Delete':
            self.model.delete_after()
        elif event.keysym == 'Left':
            self.model.move_cursor_left()
        elif event.keysym == 'Right':
            self.model.move_cursor_right()
        elif event.keysym == 'Up':
            self.model.move_cursor_up()
        elif event.keysym == 'Down':
            self.model.move_cursor_down()
        elif len(event.char) == 1:
            self.model.insert_char(event.char)

    def update_cursor_location(self, loc):
        self.draw_cursor(loc)

    def update_text(self):
        self.draw_ui()

    def draw_ui(self):
        self.delete('all')
        self.cursor = None
        self.write_out_lines()
        self.draw_cursor(self.model.cursor_location)

    def write_out_lines(self):
        y = 0
        for i, line in enumerate(self.model.all_lines()):
            self.create_text(5, y, anchor='nw', text=line, font=self.font)
            y += self.line_height

    def draw_cursor(self, loc):
        cursor_x = self.left_padding + loc.column * self.char_width
        cursor_y = loc.row * self.line_height

        if self.cursor:
            self.coords(self.cursor, cursor_x, cursor_y, cursor_x, cursor_y + self.line_height)
        else:
            self.cursor = self.create_line(cursor_x, cursor_y, cursor_x, cursor_y + self.line_height, fill='red',
                                           tags=('cursor',)
                                           )


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
        self.selection_range: LocationRange | None = None
        self.cursor_location: Location = Location(0, 0)
        self.cursor_observers: list[CursorObserver] = []
        self.text_observers: list[TextObserver] = []

    def all_lines(self):
        return iter(self.lines)

    def lines_range(self, start, end):
        return iter(self.lines[start:end])

    def add_cursor_observer(self, obs: CursorObserver):
        self.cursor_observers.append(obs)

    def remove_cursor_observer(self, obs: CursorObserver):
        self.cursor_observers.remove(obs)

    def notify_cursor_observers(self):
        [obs.update_cursor_location(self.cursor_location) for obs in self.cursor_observers]

    def move_cursor_left(self):
        self.move_cursor(-1, 0)

    def move_cursor_right(self):
        self.move_cursor(1, 0)

    def move_cursor_up(self):
        self.move_cursor(0, -1)

    def move_cursor_down(self):
        self.move_cursor(0, 1)

    def move_cursor(self, dx, dy):
        old_row = self.cursor_location.row
        old_col = self.cursor_location.column

        new_row = self.cursor_location.row + dy
        new_col = self.cursor_location.column + dx

        # Ensure we don't go out of bounds vertically
        new_row = max(0, min(new_row, len(self.lines) - 1))

        # Handle moving left at the beginning of a line
        if dx < 0 and new_col < 0 and new_row > 0:
            new_row -= 1
            new_col = len(self.lines[new_row])
        # Handle moving right at the end of a line
        elif dx > 0 and new_col > len(self.lines[new_row]) and new_row < len(self.lines) - 1:
            new_row += 1
            new_col = 0
        else:
            # Ensure we don't go out of bounds horizontally
            new_col = max(0, min(new_col, len(self.lines[new_row])))

        self.cursor_location = Location(new_row, new_col)

        if not (old_row == new_row and old_col == new_col):
            self.notify_cursor_observers()

    def add_text_observer(self, obs: TextObserver):
        self.text_observers.append(obs)

    def remove_text_observer(self, obs: TextObserver):
        self.text_observers.remove(obs)

    def notify_text_observers(self):
        [obs.update_text() for obs in self.text_observers]

    def delete_before(self):
        if self.selection_range:
            self.delete_range(self.selection_range)
            return

        row = self.cursor_location.row
        column = self.cursor_location.column

        if column > 0:
            self.lines[row] = self.lines[row][:column - 1] + self.lines[row][column:]
            self.move_cursor_left()

        elif row > 0:
            self.move_cursor_left()
            self.lines[row - 1] += self.lines[row]
            del self.lines[row]

        self.notify_text_observers()

    def delete_after(self):
        if self.selection_range:
            self.delete_range(self.selection_range)
            return

        row = self.cursor_location.row
        column = self.cursor_location.column

        if column == len(self.lines[row]) and row < len(self.lines) - 1:
            self.lines[row] += self.lines[row + 1]
            del self.lines[row + 1]
            self.notify_text_observers()
            return

        self.lines[row] = self.lines[row][:column] + self.lines[row][column + 1:]
        self.notify_text_observers()

    def delete_range(self, r: LocationRange):
        pass

    def get_selection_range(self) -> LocationRange:
        return self.selection_range

    def set_selection_range(self, r: LocationRange):
        self.selection_range = r

    def insert_newline(self):
        row = self.cursor_location.row
        column = self.cursor_location.column

        current_line = self.lines[row]
        self.lines[row] = current_line[:column]
        self.lines.insert(row + 1, current_line[column:])

        self.cursor_location = Location(row + 1, 0)

        self.notify_cursor_observers()
        self.notify_text_observers()

    # def backspace(self):
    #     row = self.model.cursor_location.row
    #     column = self.model.cursor_location.column
    #
    #     if column > 0:
    #         self.model.lines[row] = self.model.lines[row][:column - 1] + self.model.lines[row][column:]
    #         self.model.cursor_location.column -= 1
    #
    #     elif row > 0:
    #         self.model.cursor_location.column = len(self.model.lines[row - 1])
    #         self.model.cursor_location.row -= 1
    #         self.model.lines[row - 1] += self.model.lines[row]
    #         del self.model.lines[row]
    #
    def insert_char(self, char):
        row = self.cursor_location.row
        column = self.cursor_location.column

        self.lines[row] = self.lines[row][:column] + char + self.lines[row][column:]
        self.cursor_location.column += 1

        self.notify_cursor_observers()
        self.notify_text_observers()


def test_text_editor_model():
    text = "First line.\nSecond line.\nThird line."
    tem = TextEditorModel(text)
    [print(line) for line in tem.lines]
    print()


def test_text_editor():
    root = Tk()
    root.title("Adriano texto edito")

    text = "First line.\nSecond line.\nThird line."
    model = TextEditorModel(text)
    editor = TextEditor(master=root, model=model)

    editor.pack()
    editor.draw_ui()
    root.mainloop()


if __name__ == "__main__":
    test_text_editor()
