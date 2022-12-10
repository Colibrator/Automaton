from tkinter import *
import time
import rules


def create_field(dimension1, dimension2, frame):
    global button_list
    if len(button_list):
        for i in button_list:
            for j in i:
                j.destroy()
    button_list.clear()
    for i in range(dimension1):
        button_list.append([])
        for j in range(dimension2):
            but = Button(frame, height=1, width=2, bg=passive_color)
            but.bind("<Button-1>", toggle)
            but.grid(row=i, column=j)
            button_list[i].append(but)


def toggle(event):
    if event.widget["bg"] == active_color:
        event.widget["bg"] = passive_color
        event.widget["fg"] = passive_color
    elif event.widget["bg"] == passive_color:
        event.widget["bg"] = active_color
        event.widget["fg"] = active_color


def run():
    lab_pause.config(text="Unpaused", bg="green", fg="black")
    while not paused:
        rules.rules(x, y, button_list, passive_color, active_color)
        for i in range(x):
            for j in range(y):
                if button_list[i][j]["fg"] == passive_color:
                    button_list[i][j]["bg"] = passive_color
                elif button_list[i][j]["fg"] == active_color:
                    button_list[i][j]["bg"] = active_color
        root.update()
        time.sleep(speed)


def save_theme_menu():
    global name, branch_save_theme
    name = StringVar()
    branch_save_theme = Toplevel(root)
    entr_save_theme = Entry(branch_save_theme, textvariable=name)
    but_save_theme = Button(branch_save_theme, text="Save theme")
    but_save_theme.bind("<Button-1>", save_theme)
    lab_save_theme = Label(branch_save_theme, text="Give a title")
    lab_save_theme.pack()
    entr_save_theme.pack()
    but_save_theme.pack()


def save_theme(event):
    global paused
    pause()
    theme_savefile = open("theme_list.txt", "a")
    theme_savefile.write("\n" + name.get() + "\n")
    theme_savefile.write(passive_color + " " + active_color)
    branch_save_theme.destroy()


def save_menu(event="<Button-1>"):
    global name, branch_save
    name = StringVar()
    branch_save = Toplevel(root)
    entr_save = Entry(branch_save, textvariable=name)
    but_save = Button(branch_save, text="Save")
    but_save.bind("<Button-1>", save)
    lab_save = Label(branch_save, text="Give a title")
    lab_save.pack()
    entr_save.pack()
    but_save.pack()


def save(event):
    global paused
    pause()
    savefile = open("saves\\" + name.get() + ".txt", "w")
    savefile.write(str(x) + " " + str(y) + '\n' + '\n')
    for i in button_list:
        newline = ""
        for j in i:
            if j["bg"] == active_color:
                newline += "1"
            else:
                newline += "0"
        savefile.write(newline + '\n')
    savefile.close()
    branch_save.destroy()


def open_menu(event="<Button-1>"):
    global name, branch_open
    name = StringVar()
    branch_open = Toplevel(root)
    entr_open = Entry(branch_open, textvariable=name)
    but_open = Button(branch_open, text="Open")
    but_open.bind("<Button-1>", openf)
    lab_open = Label(branch_open, text="Write a name")
    lab_open.pack()
    entr_open.pack()
    but_open.pack()



def openf(event):
    global paused, x, y
    pause()
    openfile = open("saves\\" + name.get() + ".txt", "r")
    dimensions = openfile.readline().split()
    x = int(dimensions[0])
    y = int(dimensions[1])
    openfile.readline()
    create_field(x, y, cell_frame)
    for i in range(x):
        current_row = openfile.readline()
        for j in range(y):
            if current_row[j] == "1":
                button_list[i][j]["fg"] = active_color
                button_list[i][j]["bg"] = active_color
            root.update()
    openfile.close()
    branch_open.destroy()


def start():
    global paused
    paused = False
    run()


def pause():
    global paused
    paused = True
    lab_pause.config(text="Paused", bg="red", fg="white")


def toggle_run(event):
    global paused
    if paused:
        start()
    else:
        pause()


def faster():
    global speed
    speed = speed/2
    lab_speed["text"] = "Current speed: " + str(1 / speed) + " FPS"


def slower():
    global speed
    speed = speed*2
    lab_speed["text"] = "Current speed: " + str(1 / speed) + " FPS"


def clear():
    pause()
    for i in button_list:
        for j in i:
            j["bg"] = passive_color
            j["fg"] = passive_color


def dimensions_menu():
    global dims, branch_dim
    branch_dim = Toplevel(root)
    entr_dim = Entry(branch_dim, textvariable=dims)
    but_dim = Button(branch_dim, text="Change dimensions")
    but_dim.bind("<Button-1>", dimensions_change)
    lab_dim = Label(branch_dim, text="Enter height and width separated by \"x\"")
    lab_dim.pack()
    entr_dim.pack()
    but_dim.pack()


def dimensions_change(event):
    global x, y, dims
    l = dims.get()
    l = l.split("x")
    x = int(l[0])
    y = int(l[1])
    create_field(x, y, cell_frame)
    branch_dim.destroy()


def theme_menu():
    global col1, col2, branch_theme
    branch_theme = Toplevel(root)
    entr_color1 = Entry(branch_theme, textvariable=col1)
    entr_color2 = Entry(branch_theme, textvariable=col2)
    but_color1 = Button(branch_theme, text="Change Theme!")
    but_color1.bind("<Button-1>", theme_change)
    lab_color = Label(branch_theme, text="Enter the desired colors using HEX")
    lab_color.pack()
    entr_color1.pack()
    entr_color2.pack()
    but_color1.pack()


def theme_change(event):
    global passive_color, active_color, col1, col2
    passive_color_temp = col1.get()
    if passive_color_temp == "":
        passive_color_temp = passive_color
    active_color_temp = col2.get()
    if active_color_temp == "":
        active_color_temp = passive_color
    branch_theme.destroy()
    for i in button_list:
        for j in i:
            if j["bg"] == passive_color:
                j["bg"] = passive_color_temp
            else:
                j["bg"] = active_color_temp
    passive_color = passive_color_temp
    active_color = active_color_temp


root = Tk()
root.geometry = "400x600"
root.bind("<Control-s>", save_menu)
root.bind("<Control-o>", open_menu)
root.bind("<space>", toggle_run)

paused = True
speed = 0.5
dims = StringVar()
col1 = StringVar()
col2 = StringVar()
x = 9
y = 9
passive_color = "white"
active_color = "black"
button_dict = {}
button_list = []

cell_frame = Frame(root)
cell_frame.grid(row=0, column=0, columnspan=4)
create_field(x, y, cell_frame)



menubar = Menu(root)
root.config(menu=menubar)
root.title("Convay's Game of Life in Tkinter v.2.1")
file = Menu(menubar, tearoff=1)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='Clear', command=clear)
file.add_command(label='Save', command=save_menu)
file.add_command(label='Open', command=open_menu)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

timem = Menu(menubar, tearoff=1)
menubar.add_cascade(label='Time', menu=timem)
timem.add_command(label='Start', command=start)
timem.add_command(label='Pause', command=pause)
timem.add_command(label='Double Speed', command=faster)
timem.add_command(label='Half Speed', command=slower)
lab_speed = Label(root, text="Current speed: " + str(1 / speed) + " FPS")
lab_speed.grid(row=1, column=0)
lab_pause = Label(root, text="Paused", bg="red", fg="white")
lab_pause.grid(row=1, column=1)

view = Menu(menubar, tearoff=1)
menubar.add_cascade(label='View', menu=view)
view.add_command(label='Change Dimensions', command=dimensions_menu)
theme = Menu(view, tearoff=0)
view.add_cascade(label="Theme...", menu=theme)
theme.add_command(label='Change Theme', command=theme_menu)
theme.add_command(label='Save Current Theme', command=save_theme_menu)



root.mainloop()
