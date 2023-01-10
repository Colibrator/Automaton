from tkinter import *
import time
import rules
import winfo
import os

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
    global gen
    lab_pause.config(text="Unpaused", bg="green", fg="black")
    while not paused:
        is_changed = False
        rules.rules(x, y, button_list, passive_color, active_color)
        for i in range(x):
            for j in range(y):
                if button_list[i][j]["fg"] == passive_color and button_list[i][j]["bg"] == active_color:
                    is_changed = True
                    button_list[i][j]["bg"] = passive_color
                elif button_list[i][j]["fg"] == active_color and button_list[i][j]["bg"] == passive_color:
                    is_changed = True
                    button_list[i][j]["bg"] = active_color
        if is_changed:
            gen += 1
            lab_generations["text"] = "Generations Elapsed: " + str(gen)
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
    theme_savefile.close()
    branch_save_theme.destroy()


def open_theme_menu():
    global name, branch_open_theme
    name = StringVar()
    branch_open_theme = Toplevel(root)
    entr_open_theme = Entry(branch_open_theme, textvariable=name)
    but_opentheme = Button(branch_open_theme, text="Open theme")
    but_opentheme.bind("<Button-1>", open_theme)
    lab_opentheme = Label(branch_open_theme, text="Write the name of your theme")
    lab_opentheme.pack()
    entr_open_theme.pack()
    but_opentheme.pack() 


def open_theme(event):
    global paused, passive_color, active_color, button_list
    pause()
    theme_openfile = open("theme_list.txt", "r")
    current_check = theme_openfile.readline().strip()
    theme_name = name.get()
    passive_color_temp = passive_color
    active_color_temp = active_color
    while current_check != theme_name and current_check != '':
        theme_openfile.readline()
        current_check = theme_openfile.readline().strip()
    if current_check == theme_name:
        color_list = theme_openfile.readline().split()
        passive_color_temp = color_list[0]
        active_color_temp = color_list[1].strip()
    elif current_check == '':
        branch_exeption = Toplevel(root)
        lab_exeption = Label(branch_exeption, text="There is no theme called {theme_name}")
        but_exeption = Button(branch_exeption, text="OK", command=branch_exeption.destroy)
        lab_exeption.pack()
        but_exeption.pack()
    for i in button_list:
        for j in i:
            if j["bg"] == passive_color:
                j["bg"] = passive_color_temp
            else:
                j["bg"] = active_color_temp
    passive_color = passive_color_temp
    active_color = active_color_temp
    branch_open_theme.destroy()


def save_menu(event="<Button-1>"):
    global name, branch_save
    name = StringVar()
    branch_save = Toplevel(root)
    entr_save = Entry(branch_save, textvariable=name)
    saves_list = Listbox(branch_save)
    file_no = 0
    for source, dir, files in os.walk(r"C:\Users\sorok\PycharmProjects\automaton\saves"):
        for name in files:
            if name.endswith((".fld")):
                saves_list.insert(file_no, name[:-4])
                file_no += 1
    but_save = Button(branch_save, text="Save")
    but_save.bind("<Button-1>", save_outer)
    lab_save = Label(branch_save, text="Give a title")
    lab_save.pack()
    saves_list.pack()
    entr_save.pack()
    but_save.pack()
    branch_save.bind("<Return>", save_outer)


def save_outer(event):
    global paused, branch_warning
    pause()
    try:
        open("saves\\" + name.get() + ".fld", "r")
    except:
        save_inner()
    else:
        branch_warning = winfo.Info(root, "w")
        branch_warning.set_notice("Are you sure you want to overwrite\nthe file that already exists?")
        but_warning = Button(branch_warning, text="OK")
        but_warning.bind("<Button-1>", save_inner)
        but_warning.grid(row=1, column=0)
        but_cancel = Button(branch_warning, text="Cancel", command=branch_warning.dismiss)
        but_cancel.grid(row=1, column=2)


def save_inner(event="<Button-1>"):
    savefile = open("saves\\" + name.get() + ".fld", "w")
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
    try:
        branch_warning.dismiss()
    except:
        pass


def open_menu(event="<Button-1>"):
    global name, branch_open, lab_open
    name = StringVar()
    branch_open = Toplevel(root)
    entr_open = Entry(branch_open, textvariable=name)
    saves_list = Listbox(branch_save)
    file_no = 0
    for source, dir, files in os.walk(r"C:\Users\sorok\PycharmProjects\automaton\saves"):
        for name in files:
            if name.endswith((".fld")):
                saves_list.insert(file_no, name[:-4])
                file_no += 1
    but_open = Button(branch_open, text="Open")
    but_open.bind("<Button-1>", openf)
    lab_open = Label(branch_open, text="Write a name")
    lab_open.pack()
    saves_list.pack()
    entr_open.pack()
    but_open.pack()
    branch_open.bind("<Return>", openf)


def openf(event):
    global paused, x, y
    pause()
    try:
        openfile = open("saves\\" + name.get() + ".fld", "r")
    except:
        lab_open.config(text="There is no such a file with name %s.fld" % name.get())
    else:
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
x = 20
y = 20
gen = 0
passive_color = "white"
active_color = "black"
button_dict = {}
button_list = []

cell_frame = Frame(root)
cell_frame.grid(row=0, column=0, columnspan=4)
create_field(x, y, cell_frame)



menubar = Menu(root)
root.config(menu=menubar)
root.title("Convay's Game of Life in Tkinter v.2.0.4")
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
lab_generations = Label(root, text="Generations Elapsed: " + str(gen))
lab_generations.grid(row=1, column=2)

view = Menu(menubar, tearoff=1)
menubar.add_cascade(label='View', menu=view)
view.add_command(label='Change Dimensions', command=dimensions_menu)
theme = Menu(view, tearoff=0)
view.add_cascade(label="Theme...", menu=theme)
theme.add_command(label='Change Theme', command=theme_menu)
theme.add_command(label='Save Current Theme', command=save_theme_menu)
theme.add_command(label='Open Theme', command=open_theme_menu)



root.mainloop()
