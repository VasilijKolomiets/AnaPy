"""
Created on Mon Dec 20 17:03:09 2021

@author: manager
"""
from settings import from_server_connect

import tkinter as tk
from tkinter import ttk

# global glob_params


def get_data_for_qombo_list():

    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = 'SELECT id, company_name FROM companies WHERE is_active'
    _cursor.execute(command_pattern)  # SQL command executing

    selected_data = _cursor.fetchall()

    cnx.commit()
    cnx.close()
    return selected_data


def f_client_select():
    def save_quit():
        global glob_params

        selected_data_row = comboExample.get()
        print(comboExample.current(), _clients_row)

        glob_params['client']['id_companies'] = int(selected_data_row[0])
        glob_params['client']['name'] = selected_data_row[1]

        app_client_pick.destroy()
    # - mainloop combo select

    _clients_row = None

    combo_list_values = get_data_for_qombo_list()

    app_client_pick = tk.Tk()
    app_client_pick.geometry('200x120')

    labelTop = ttk.Label(app_client_pick,  text="Виберіть Клієнта")
    labelTop.grid(column=0, row=0, pady=5, padx=15)

    confirm_button = ttk.Button(app_client_pick, text='Вибрати й завершити', command=save_quit)
    confirm_button.grid(column=0, row=1, pady=15)

    comboExample = ttk.Combobox(app_client_pick,
                                values=combo_list_values,
                                state="readonly",
                                )

    comboExample.grid(column=0, row=2, pady=5, padx=15)
    comboExample.current(1)

    app_client_pick.mainloop()
