from tkinter import *
class Info(Toplevel):
    
    def __init__(self, screen, type):
        super(Info, self).__init__(screen)
        self.type = type
        self.lab_notice = Label(self, text="default")
        self.lab_notice.grid(row=0, column=1, columnspan=2)
        if self.type == "w":
            self.icon = PhotoImage(file="warn.gif")
            self.title("Warning!")
        elif self.type == "e":
            self.icon = PhotoImage(file="skull.png")
            self.title("Fatal!")
        self.fr_icon = Frame(self)
        self.fr_icon.grid(row=0, column=0)
        self.lab_icon = Label(self.fr_icon, image=self.icon)
        self.lab_icon.photo = self.icon
        self.lab_icon.pack()


    def dismiss(self):
        self.destroy()

    def set_notice(self, txt):
        self.lab_notice.config(text=txt)

    