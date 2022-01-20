# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 14:31:07 2021

@author: Vasil
"""
import tkinter as tk

root = tk.Tk()
label = tk.Label(root)
listbox = tk.Listbox(root)
label.pack(side="bottom", fill="x")
listbox.pack(side="top", fill="both", expand=True)

listbox.insert("end", "one", "two", "three", "four", "five")

def callback(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        label.configure(text=data)
    else:
        label.configure(text="")

listbox.bind("<<ListboxSelect>>", callback)

root.mainloop()