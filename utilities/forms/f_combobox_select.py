# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 13:12:16 2021

@author: manager
"""
import tkinter as tk
from tkinter import ttk

from settings import state_params


def f_combobox_select(geometry: str = '450x278', text_message: str = "Виберіть Клієнта",
                      combo_list_values: list = [],
                      select_field_width=30,
                      save_quit_processing=None):
    """
    Select item from 'combo_list_values' and procees in in 'save_quit' function.

    :param geometry: DESCRIPTION, defaults to '300x185'
    :type geometry: str, optional
    :param text_message: DESCRIPTION, defaults to "Виберіть Клієнта"
    :type text_message: str, optional
    :param combo_list_values: DESCRIPTION, defaults to []
    :type combo_list_values: list, optional
    :param save_quit_processing: DESCRIPTION, defaults to None
    :type save_quit: function, have to process picked item and destroy "app_item_pick.mainloop()"
    :return: DESCRIPTION
    :rtype: TYPE

    """
    def save_quit():
        global state_params

        selected_data_row = comboExample.get()
        print(comboExample.current(), selected_data_row)

        save_quit_processing(state_params, selected_data_row)

        app_item_pick.destroy()
        app_item_pick.quit()
    # - mainloop combo select

    app_item_pick = tk.Toplevel()  # tk.Tk()
    app_item_pick.geometry(geometry)   # fi = 1.618

    labelTop = ttk.Label(app_item_pick,  text=text_message)
    labelTop.grid(column=0, row=0, pady=5, padx=15)

    confirm_button = ttk.Button(app_item_pick, text='Вибрати й завершити', command=save_quit)
    confirm_button.grid(column=0, row=1, pady=15)

    comboExample = ttk.Combobox(app_item_pick,
                                width=select_field_width,
                                values=combo_list_values,
                                state="readonly",
                                )

    comboExample.grid(column=0, row=2, pady=5, padx=15)
    comboExample.current(0)

    app_item_pick.focus_force()

    app_item_pick.mainloop()
