# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 20:43:07 2021

@author: Vasil
"""

import tkinter as tk
from tkinter import ttk

# Create an empty Tkinter window
root = tk.Tk()
root_frm = ttk.Frame(root)

root_frm = ttk.Frame(root, padding="3 3 2 2")
# grid(column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
root_frm.pack(side=tk.BOTTOM, fill=tk.X)


def from_kg():
    # Get user value from input box and multiply by 1000 to get kilograms
    gram = float(e2_value.get())*1000

    # Get user value from input box and multiply by 2.20462 to get pounds
    pound = float(e2_value.get())*2.20462

    # Get user value from input box and multiply by 35.274 to get ounces
    ounce = float(e2_value.get())*35.274

    # Empty the Text boxes if they had text from the previous use and fill them again
    t1.delete("1.0", tk.END)  # Deletes the content of the Text box from start to END
    t1.insert(tk.END, gram)  # Fill in the text box with the value of gram variable
    t2.delete("1.0", tk.END)
    t2.insert(tk.END, pound)
    t3.delete("1.0", tk.END)
    t3.insert(tk.END, ounce)


# Create a Label widget with "Kg" as label
e1 = ttk.Label(root_frm, text="Kg")
e1.grid(row=0, column=0)  # The Label is placed in position 0, 0 in the window

e2_value = tk.StringVar()  # Create a special StringVar object
e2 = ttk.Entry(root_frm, textvariable=e2_value)  # Create an Entry box for users to enter the value
e2.grid(row=0, column=1)

# Create a button widget
# The from_kg() function is called when the button is pushed
b1 = ttk.Button(root_frm, text="Convert", command=from_kg)
b1.grid(row=0, column=2)

# Create three empty text boxes, t1, t2, and t3
t1 = tk.Text(root_frm, height=1, width=20)
t1.grid(row=1, column=0)

t2 = tk.Text(root_frm, height=1, width=20)
t2.grid(row=1, column=1)

t3 = tk.Text(root_frm, height=1, width=20)
t3.grid(row=1, column=2)

# This makes sure to keep the main window open
root.mainloop()
