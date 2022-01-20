# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:05:47 2021

@author: Vasyl Kolomiiets
"""
# =============================================================================
#
#   https://python-scripts.com/tkinter
# =============================================================================


import winsound
from utilities.forms.f_devivery_points import form_delivery_point_add
# from utilities.forms.f_client_select import f_client_select

from settings import from_server_connect

import tkinter as tk
from tkinter.filedialog import askopenfilename  # , asksaveasfilename
from tkinter import ttk

# global temp_cursor
# global glob_params

# temp_cursor = None
glob_params = dict(
    client=dict(id_companies=None, name=None),
    delivery_contract=dict(id_delivery_contract=None, text=None),
    postservice=dict(postservice_id=None, name=None),

)


def f_client_select():

    def get_data_for_company_combo_list():

        cnx = from_server_connect()
        _cursor = cnx.cursor()   # used inside f-function

        command_pattern = 'SELECT id, company_name, short_name_latin FROM companies WHERE is_active'
        _cursor.execute(command_pattern)  # SQL command executing

        selected_data = _cursor.fetchall()

        cnx.commit()
        cnx.close()
        return selected_data

    def save_quit():
        global glob_params

        selected_data_row = comboExample.get()
        print(comboExample.current(), _clients_row)

        glob_params['client']['id_companies'] = int(selected_data_row.split()[0])
        glob_params['client']['name'] = selected_data_row.split()[1]

        app_client_pick.destroy()
        app_client_pick.quit()
    # - mainloop combo select

    _clients_row = None

    combo_list_values = get_data_for_company_combo_list()

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


def f_contract_select():

    def get_data_for_company_combo_list():

        cnx = from_server_connect()
        _cursor = cnx.cursor()   # used inside f-function

        command_pattern = 'SELECT id_waybills,  FROM delivery_contracts, name WHERE is_active'
        _cursor.execute(command_pattern)  # SQL command executing

        selected_data = _cursor.fetchall()

        cnx.commit()
        cnx.close()
        return selected_data

    def save_quit():
        global glob_params

        selected_data_row = comboExample.get()
        print(comboExample.current(), _clients_row)

        glob_params['delivery_contract']['id_delivery_contract'] = int(
            selected_data_row.split()[0])
        glob_params['delivery_contract']['name'] = selected_data_row.split()[1]

        app_client_pick.destroy()
        app_client_pick.quit()
    # - mainloop combo select

    _clients_row = None

    combo_list_values = get_data_for_company_combo_list()

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


"""
'SystemAsterisk'
'SystemExclamation'
'SystemExit'
'SystemHand'
'SystemQuestion'

import winsound
freq = 2500 # Set frequency To 2500 Hertz
dur = 1000 # Set duration To 1000 ms == 1 second
winsound.Beep(freq, dur)

freq = 100
dur = 50

# loop iterates 5 times i.e, 5 beeps will be produced.
for i in range(0, 5):
    winsound.Beep(freq, dur)
    freq+= 100
    dur+= 50
"""
# from utilities.forms.delivery_point import delivery_point_editing


def do_all():
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    z = askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))


def activate_Створити():
    global mainmenu
    global glob_params
    print('Створити')
    f_client_select()  # glob_params["client"] forming

    lbl_statusbar.config(text=F"Клієнт:: {glob_params['client']['name']}")
    #  var_lbl_statusbar.set("Тут будуть підказки…")
    mainmenu.entryconfigure("Імпортувати", state=tk.NORMAL)  # ['state'] = 'normal'


root = tk.Tk()

root.minsize(1000, 500)
root.title('PostMan')

mainframe = ttk.Frame(root, padding="2 5 2 2")
# grid(column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.pack(side=tk.BOTTOM, fill=tk.X)

mainmenu = tk.Menu(mainframe)
root.config(menu=mainmenu)

# sysmenu = tk.Menu(mainmenu, name='system', tearoff=0)

env_params_menu = tk.Menu(mainmenu, tearoff=0)
env_params_menu.add_command(label="Клієнт", command=activate_Створити)
env_params_menu.add_command(label="Поставка", command=f_contract_select)
env_params_menu.add_command(label="Перевізник", command=None)

create_menu = tk.Menu(mainmenu, tearoff=0)
create_menu.add_command(label="... поставку")
create_menu.add_command(label="... точку доставки",
                        command=form_delivery_point_add)  # delivery_point_editing

import_menu = tk.Menu(mainmenu, tearoff=0)
import_menu.add_command(label="... продукцію")
import_menu.add_command(label="... нові точки")
import_menu.add_command(label="... розподіл відправлень", command=do_all)

export_menu = tk.Menu(mainmenu, tearoff=0)
export_menu.add_command(label="... продукцію")
export_menu.add_command(label="... точки отримання")
export_menu.add_command(label="... розподіл відправлень")


editing_menu = tk.Menu(mainmenu, tearoff=0)
editing_menu.add_command(label="... одержувача")
editing_menu.add_command(label="... місто / вулицю")

create_tickets_menu = tk.Menu(mainmenu, tearoff=0)

exit_menu = tk.Menu(mainmenu, tearoff=0)
# .quit - close frame - do not stop root
exit_menu.add_command(label="Закрити програму", command=root.destroy)  # root.quit

mainmenu.add_cascade(label="Параметри оточення", menu=env_params_menu)
mainmenu.add_cascade(label="Створити", menu=create_menu)
mainmenu.add_cascade(label="Імпортувати", menu=import_menu)
mainmenu.add_cascade(label="Правка", menu=editing_menu)
mainmenu.add_cascade(label="Експорт даних", menu=export_menu)
mainmenu.add_cascade(label="Експрес Накладні", menu=create_tickets_menu)
mainmenu.add_cascade(label="Вихід", menu=exit_menu)
# mainmenu.add_cascade(menu=sysmenu)

mainmenu.entryconfigure("Імпортувати", state=tk.DISABLED)

var_lbl_statusbar = tk.StringVar()
var_lbl_statusbar.set("Тут будуть підказки…")
# lbl_statusbar = tk.Label(mainframe, text="Тут будуть підказки…",
#                          relief=tk.SUNKEN, anchor=tk.W,
#                          # style=,
#                          )  # bd=1,

lbl_statusbar = ttk.Label(mainframe, text="Тут будуть підказки…",
                          relief=tk.SUNKEN, anchor=tk.W,
                          textvariable=var_lbl_statusbar,
                          # style=,
                          )  # bd=1,
lbl_statusbar.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)


root.mainloop()
