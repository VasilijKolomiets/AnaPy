# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 07:32:39 2021

@author: Vasil
"""

from pprint import pprint
import tkinter as tk
from tkinter import ttk

global combo_pick


def save_quit():
    global combo_pick
    print(comboExample.current(), comboExample.get())
    combo_pick = comboExample.current()
    app.destroy()


app = tk.Tk()
app.geometry('200x120')

labelTop = tk.Label(app,  text="Choose your favourite month")
labelTop.grid(column=0, row=0, pady=5)

confirm_button = tk.Button(app, text='Вибрати й завершити', command=save_quit)
confirm_button.grid(column=0, row=1, pady=10)


comboExample = ttk.Combobox(app,
                            values=[
                                "January",  "February", "March", "April",
                                "May",  "June", "July", "Augest",
                                "January",  "February", "March", "April",
                            ],
                            state="readonly"
                            )


comboExample.grid(column=0, row=2, pady=5)
comboExample.current(1)

app.mainloop()


# -----------------------------------------------------------------------------


app = tk.Tk()
app.geometry('200x100')

labelTop = tk.Label(app,  text="Choose your favourite month")
labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app,
                            values=[
                                "January",
                                "February",
                                "March",
                                "April"])
pprint(dict(comboExample))
comboExample.grid(column=0, row=1)
comboExample.current(1)

print(comboExample.current(), comboExample.get())

app.mainloop()


# ----------------------------------------------------------------------------


global combo_pick


def callbackFunc(event):
    print("New Element Selected", comboExample.current(), comboExample.get())


def save_quit():
    global combo_pick
    combo_pick = comboExample.current()
    app.destroy()


app = tk.Tk()
app.geometry('200x200')

labelTop = tk.Label(app,  text="Choose your favourite month")
labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app,
                            values=[
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",
                                "January",  "February", "March", "April",


                            ],
                            state="readonly"
                            )


comboExample.grid(column=0, row=1)
comboExample.current(0)

comboExample.bind("<<ComboboxSelected>>", callbackFunc)

confirm_button = tk.Button(app, text='Вибрати', command=save_quit)
confirm_button.grid(column=0, row=2, pady=70)


app.mainloop()


# ----------------------------------------  dynamicly combolist changimg  -----------------------


def callbackFunc(event):
    print("New Element Selected")


app = tk.Tk()
app.geometry('200x100')


def changeMonth():
    comboExample["values"] = ["July",
                              "August",
                              "September",
                              "October"
                              ]


labelTop = tk.Label(app, text="Choose your favourite month")
labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app,
                            values=[
                                "January",
                                "February",
                                "March",
                                "April"],
                            postcommand=changeMonth)


comboExample.grid(column=0, row=1)

app.mainloop()
