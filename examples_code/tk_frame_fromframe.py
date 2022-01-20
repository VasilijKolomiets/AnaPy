import tkinter as tk
from tkinter import ttk


def about():
    a = tk.Toplevel()
    a.geometry('200x150')
    a['bg'] = 'grey'
    a.overrideredirect(True)
    ttk.Label(a, text="About this").pack(expand=1)
    a.after(5000, lambda: a.destroy())


root = tk.Tk()
root.title("Главное окно")
tk.Button(text="Button", width=20).pack()
tk.Label(text="Label", width=20, height=3).pack()
tk.Button(text="About", width=20, command=about).pack()

root.mainloop()
