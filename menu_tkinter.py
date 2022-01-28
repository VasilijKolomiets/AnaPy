# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 14:05:47 2021

@author: manager
"""
# =============================================================================
#
#   https://python-scripts.com/tkinter
# =============================================================================
from functools import partial  # TODO: replace lambda(s)

import tkinter as tk
from tkinter import ttk

import winsound

import utilities.utils  # do not del this import !!

from utilities.forms.f_delivery_points import f_delivery_point_add
from utilities.forms.f_new_points_file_reading import f_new_points_file_reading
from utilities.forms.f_new_items_file_reading import f_new_items_file_reading
from utilities.forms.f_new_items_appointts_file_reading import f_new_items_appointts_file_reading
from utilities.forms.f_combobox_select import f_combobox_select
from utilities.forms.f_create_tickets import f_create_tickets
from utilities.forms.f_create_reestr import f_create_reestr
from utilities.forms.f_create_waybills_pdf import f_create_waybills_pdf
from utilities.forms.easy_form import easy_form
from utilities.sql_base_utils import f_cities_refresh, f_streets_refresh

from settings import state_params, credentials, widgets_table
import ua_posts_api

from model import select_fields_from_table
"""
def easy_form(
        widget_dict: dict = dict(),
        entered_data_processing=add_row_values_to_DB,  # by default, save new row data to DB table
        params_tuple_for_partical: tuple = tuple()     # DB table name OR  DB table name & row ID
) -> None:
"""


def f_client_select():

    def processing(state_params, selected_data_row):
        fields = selected_data_row.split()
        state_params['client']['id_companies'] = int(fields[0])
        state_params['client']['name'] = fields[-1]
        state_params['client']['fullname'] = fields[1]

    combo_list_values = select_fields_from_table()
    f_combobox_select(
        combo_list_values=combo_list_values,
        save_quit_processing=processing
    )


def f_contract_select():

    def processing(state_params, selected_data_row):
        state_params['delivery_contract']['id_delivery_contract'] = int(
            selected_data_row.split()[0])
        state_params['delivery_contract']['name'] = selected_data_row.split(maxsplit=1)[-1]

        state_params['post_service']['id_postcervices'] = int(
            selected_data_row.rsplit(maxsplit=1)[-1])

        state_params['statusbar'].set(
            state_params['statusbar'].get()
            + F". Контракт: {state_params['delivery_contract']['name']}"
        )

    combo_list_values = select_fields_from_table(
        fields='id_delivery_contract, name, postservice_id',
        table='delivery_contracts',
        where_condition=F"is_active AND id_companies = {state_params['client']['id_companies']}"
    )

    f_combobox_select(
        combo_list_values=combo_list_values,
        save_quit_processing=processing
    )


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


def client_select():
    global mainmenu
    global state_params
    print('Створити')
    f_client_select()  # glob_params["client"] forming

    var_lbl_statusbar.set(F"Клієнт:: {state_params['client']['name']}")
    mainmenu.entryconfigure("Імпортувати", state=tk.NORMAL)  # ['state'] = 'normal'


if __name__ == '__main__':
    post_service_credentials = credentials['Meest']
    postman = ua_posts_api.Postman(post_service_credentials)

    root = tk.Tk()

    root.minsize(1000, 500)
    root.title('PostMan')
    root.option_add("*Font", 'Verdana 14')

    mainframe = ttk.Frame(root, padding="2 5 2 2")
    # grid(column=0, row=2, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.pack(side=tk.BOTTOM, fill=tk.X)

    mainmenu = tk.Menu(mainframe)
    mainmenu.option_add("*Font", 'Verdana 14')
    root.config(menu=mainmenu)

    # sysmenu = tk.Menu(mainmenu, name='system', tearoff=0)

    env_params_menu = tk.Menu(mainmenu, tearoff=0)
    env_params_menu.add_command(label="Клієнт", command=client_select)
    env_params_menu.add_command(label="Поставка", command=f_contract_select)
    env_params_menu.add_separator()
    env_params_menu.add_command(
        label="Завантажити токени міст",
        command=partial(f_cities_refresh, state_params)
    )
    env_params_menu.add_command(label="Завантажити токени вулиць", command=f_streets_refresh)

    create_menu = tk.Menu(mainmenu, tearoff=0)
    create_menu.add_command(label="... точку доставки",
                            command=f_delivery_point_add)  # delivery_point_adding
    create_menu.add_command(
        label="... поставку",
        command=partial(
            easy_form, widgets_table['delivery_contracts'],
            ('delivery_contracts',)
        )
    )

    create_menu.add_command(
        label="... Клієнта",
        command=partial(
            easy_form, widgets_table['companies'],
            ('companies',)
        )

    )
    create_menu.add_command(label="... Перевізника")

    import_menu = tk.Menu(mainmenu, tearoff=0)
    import_menu.add_command(
        label="... продукцію",
        command=partial(f_new_items_file_reading, state_params)
    )
    import_menu.add_command(
        label="... нові точки",
        command=partial(f_new_points_file_reading, postman, state_params)
    )
    import_menu.add_command(
        label="... розподіл відправлень",
        command=partial(f_new_items_appointts_file_reading, state_params)
    )

    export_menu = tk.Menu(mainmenu, tearoff=0)
    export_menu.add_command(label="... продукцію")
    export_menu.add_command(label="... точки отримання")
    export_menu.add_command(label="... розподіл відправлень")
    export_menu.add_command(
        label="... PDF експрес-накладні",
        command=partial(f_create_waybills_pdf, postman, state_params)
    )

    editing_menu = tk.Menu(mainmenu, tearoff=0)
    editing_menu.add_command(label="... одержувача")
    editing_menu.add_command(label="... місто / вулицю")

    create_tickets_menu = tk.Menu(mainmenu, tearoff=0)
    create_tickets_menu.add_command(
        label="... створити ЕН",
        command=partial(f_create_tickets, postman, state_params)
    )
    create_tickets_menu.add_command(
        label="... створити Реєстр",
        command=partial(f_create_reestr, postman, state_params)
    )

    exit_menu = tk.Menu(mainmenu, tearoff=0)
    # .quit - close frame - do not stop root
    exit_menu.add_command(label="Закрити програму", command=root.destroy)  # root.quit

    mainmenu.add_cascade(label="Параметри оточення", menu=env_params_menu)
    mainmenu.add_cascade(label="Створити", menu=create_menu)
    mainmenu.add_cascade(label="Імпортувати", menu=import_menu)
    mainmenu.add_cascade(label="Правка", menu=editing_menu)
    mainmenu.add_cascade(label="Експорт даних", menu=export_menu)
    mainmenu.add_cascade(label="Поштові документи", menu=create_tickets_menu)
    mainmenu.add_cascade(label="Вихід", menu=exit_menu)
    # mainmenu.add_cascade(menu=sysmenu)

    mainmenu.entryconfigure("Імпортувати", state=tk.DISABLED)

    var_lbl_statusbar = tk.StringVar()
    var_lbl_statusbar.set("Тут будуть підказки…")

    lbl_statusbar = ttk.Label(mainframe, text="Тут будуть підказки…",
                              relief=tk.SUNKEN, anchor=tk.W,
                              textvariable=var_lbl_statusbar,
                              # style=,
                              )  # bd=1,
    state_params['statusbar'] = var_lbl_statusbar
    lbl_statusbar.pack(side=tk.BOTTOM, padx=1, pady=1, fill=tk.X)

    root.mainloop()
