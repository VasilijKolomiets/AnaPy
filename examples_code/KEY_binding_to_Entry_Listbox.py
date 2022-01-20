# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:46:01 2021

@author: Vasil
"""

import tkinter as tk
from tkinter import ttk


def on_change_selection(event):
    # перенос выбранного из списка значения в окно ввода
    selection = event.widget.curselection()
    global var_entry_text
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        var_entry_text.set(data)
        filter_listbox(event)


def create_listbox(event):
    # создание выпадающего окна со списком языков. Может нужен OnTop() ?
    global city_start_values_list
    global city_listbox, listbox_values
    print("box creating")

    list_root = tk.Tk()
    listbox_values = tk.Variable(master=list_root)  # list_root
    listbox_values.set(city_start_values_list)
    city_listbox = tk.Listbox(list_root, listvariable=listbox_values)
    city_listbox.bind('<<ListboxSelect>>', on_change_selection)

    if var_entry_text.get() != '':
        filter_listbox(event)

    city_listbox.pack()
    list_root.mainloop()


def filter_listbox(event):
    global city_start_values_list
    global city_listbox, listbox_values

    entered_text = ent_lookup.get().lower()
    z = str(entered_text)
    if not city_listbox:  # выпадающий список еще не создан
        create_listbox(event)

    if not listbox_values:
        return
    if entered_text == '':
        listbox_values.set(city_start_values_list)
        # city_listbox["values"] = city_start_values_list
    else:
        # фильтруем значения, начинающиеся с подстроки
        values = [el for el in city_start_values_list if el.lower().startswith(entered_text)]
        # city_listbox["values"] = values
        listbox_values.set(values)

    print(ent_lookup.get())


# основная программа - задание поля ввода с описанием. binding обработчиков
city_listbox, listbox_values = None, None

city_start_values_list = [
    'C', 'C++', 'Java',
    'Python', 'Perl',
    'PHP', 'ASP', 'JS'
]


root = tk.Tk()
root.minsize(170, 100)

mainframe = ttk.Frame(root, padding="2 5 2 2")
mainframe.pack(side=tk.BOTTOM, fill=tk.X)

lbl_lookup = ttk.Label(mainframe, text='real')
lbl_lookup.pack(side=tk.LEFT)

var_entry_text = tk.StringVar(root)
var_entry_text.set('')
ent_lookup = ttk.Entry(mainframe, width=30, textvariable=var_entry_text)
ent_lookup.pack(side=tk.RIGHT)

ent_lookup.bind('<Button-3>', create_listbox)
ent_lookup.bind('<KeyRelease>', filter_listbox)  # '<Key>'

root.mainloop()


# ------------------------------------------------------------------------------------------------
