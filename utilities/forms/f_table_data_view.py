# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 19:15:33 2021

@author: https://www.pythontutorial.net/tkinter/tkinter-treeview/
"""
from functools import partial

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


def my_inner_fun(row):
    showinfo(title='Information', message=','.join(row))


class TreeTable(tk.Tk):
    def __init__(self, title='TreeTableView', size='920x400', cols_names=None, table_data=None,
                 process_selection=None):
        super().__init__()

        self.title(title)
        self.geometry(size)
        # self.configure(scrollregion=self.bbox("all"))

        # self.item_selected = item_selected
        self.tree = self.create_tree_widget(cols_names, table_data, process_selection)

    def create_tree_widget(self, cols_names, table_data, process_selection):
        if not cols_names:
            cols_names = ["_".join(['col', str(i)]) for i in range(len(table_data[0]))]
        tree = ttk.Treeview(self, columns=cols_names, show='headings')

        # define headings
        for cols_name in cols_names:
            tree.heading(cols_name, text=cols_name)

        tree.bind('<<TreeviewSelect>>', partial(
            self.items_selected, process_row=process_selection))
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.stack[-1], orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # add data to the treeview
        for row in table_data:
            tree.insert('', tk.END, values=row)

        return tree

    def items_selected(self, event, process_row=None):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']

            # show a message
            process_row(record)


if __name__ == '__main__':
    contacts = []
    for n in range(1, 100):
        contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

    app = TreeTable(cols_names=['First', 'Last', 'e-mail'], table_data=contacts,
                    process_selection=my_inner_fun)
    app.mainloop()
