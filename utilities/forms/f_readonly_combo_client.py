
"""
Created on Mon Dec 20 17:03:09 2021

@author: manager
"""

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
