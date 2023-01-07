import tkinter as tk
from main import active_color, passive_color

active = 1
passive = 0

class Cell(tk.Button):

    def __init__(self, screen):
        super(Cell, self).__init__(screen, bg=passive_color, height=1, width=2)
        self.state = active
        self.already_changed = False

    def change(self):
        if self.state == active:
            self.state = passive
        else:
            self.state = active
            self.config(bg=active_color)

    def mouse_entered(self):
        if not self.already_changed:
            self.change()
            self.already_changed = True

    def mouse_up(self):
        self.already_changed = False


class Field(tk.Frame):
    def __init__(self, screen, width, height):
        super(Field, self).__init__(screen)

        buttons = []

        for y in range(height):
            buttons.append([])
            for x in range(width):
                button = Cell(self)
                button.grid(row = x, column = y)

                buttons[y].append(button)

        self.buttons = buttons

        self.bind_all("<Button-1>", self.mouse_down)
        self.bind_all("<ButtonRelease-1>", self.mouse_up)
        self.bind_all("<B1-Motion>", self.mouse_motion)

        self.mouse_pressed = False


    def mouse_down(self, e):
        self.update_mouse_state(e)
        self.mouse_pressed = True

    def mouse_up(self, e):
        self.mouse_pressed = False
        for row in self.buttons:
            for button in row:
                button.mouse_up()

    def mouse_motion(self, e):
        self.update_mouse_state(e)

    def update_mouse_state(self, e):
        for row in self.buttons:
            for button in row:
                if self.winfo_containing(e.x_root, e.y_root) is button:
                    button.mouse_entered()