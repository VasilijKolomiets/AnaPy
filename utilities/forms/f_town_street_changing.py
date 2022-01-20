# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 11:46:27 2021

@author: Vasil
"""
from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk

app = tk.Tk()
app.geometry('200x100')

labelTop = tk.Label(app,
                    text="Choose your favourite month")
labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app,
                            values=[
                                "January",
                                "February",
                                "March",
                                "April"],
                            state="readonly")

comboExample.grid(column=0, row=1)
comboExample.current(0)

print(comboExample.current(), comboExample.get())

app.mainloop()

# import tkinter as tk
# from tkinter import ttk

OptionList = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer"
]

app = tk.Tk()

app.geometry('100x200')

variable = tk.StringVar(app)
variable.set(OptionList[0])

opt = ttk.OptionMenu(app, variable, default=1, *OptionList)
opt.config(width=90)  # , font=('Helvetica', 12)
opt.pack(side="top")


labelTest = tk.Label(text="", font=('Helvetica', 12), fg='red')
labelTest.pack(side="top")


def callback(*args):
    labelTest.configure(text="The selected item is {}".format(variable.get()))


variable.trace("w", callback)

app.mainloop()


# import tkinter as tk


win = tk.Tk()
win.geometry("100x50")


def take_user_input_for_something():
    user_input = simpledialog.askstring(
        "Pop up for user input!", "What do you want to ask the user to input here?")
    if user_input != "":
        print(user_input)


menubar = tk.Menu(win)
dropDown = tk.Menu(menubar, tearoff=0)
dropDown.add_command(label="Do something", command=take_user_input_for_something)

# this entry field is not really needed her.
# however I noticed you did not define this widget correctly
# so I put this in to give you an example.
my_entry = tk.Entry(win)
my_entry.pack()

menubar.add_cascade(label="Drop Down", menu=dropDown)
win.config(menu=menubar)

win.mainloop()
