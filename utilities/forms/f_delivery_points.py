# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 20:47:34 2021

@author: Vasil
"""
# from settings import sql_connect_commit_close, sql_connect_close
from settings import from_server_connect, state_params
from utilities.forms.f_combobox_select import f_combobox_select
from utilities.utils import ФИО_to_surname_name_middlename

import tkinter as tk
# from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk

# global temp_cursor
global _widgets
# fields table
_widgets = dict(surname={'text': 'Прізвище'},
                name={'text': "Ім'я"},
                middle_name={'text': "По батькові"},
                phone={'text': "Телефон: +380 50 4522 559 "},
                city={'text': "Місто"},
                street={'text': "Вулиця"},
                building={'text': "Будинок"},
                floor={'text': "Поверх"},
                flat={'text': "№ квартири"},
                comment={'text': "Коментар"},
                # date_in
                branch={'text': "№ Відділення (якщо є)"},
                # active
                post_ZIP={'text': "Поштовий індекс"},
                )


# @sql_connect_commit_close
def add_point_to_DB():
    """Connect to BD and INSERT data."""
    global _widgets
    # global temp_cursor
    """
    'id_receivers', 'int', 'NO', 'PRI',      NULL, 'auto_increment'
    'id_companies', 'int', 'NO', 'MUL',      NULL, ''
    'surname', 'varchar(45)', 'YES', '',     NULL, ''
    'name', 'varchar(45)', 'YES', '',        NULL, ''
    'middle_name', 'varchar(45)', 'YES', '', NULL, ''
    'phone', 'varchar(19)', 'YES', '',       NULL, ''
    'city', 'varchar(45)', 'YES', '',        NULL, ''
    'street', 'varchar(45)', 'YES', '',      NULL, ''
    'building', 'varchar(5)', 'YES', '',     NULL, ''
    'floor', 'int', 'YES', '',               NULL, ''
    'flat', 'varchar(45)', 'YES', '',        NULL, ''
    'comment', 'varchar(255)', 'YES', '',    NULL, ''
    'date_in', 'date', 'YES', '',            NULL, ''
    'branch', 'varchar(45)', 'YES', '',      NULL, ''
    'active', 'tinyint', 'YES', '',          '1', ''
    'post_ZIP', 'varchar(5)', 'YES', '',     NULL, ''

    """
    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = 'INSERT INTO receivers({fields_list}) VALUES ({multi_ss})'
    # sql_command = command_pattern.format(", :".join([''] + list(_widgets.keys()))[2:])
    sql_command = command_pattern.format(
        {
            'fields_list': ", ".join(list(_widgets.keys())),
            'multi_ss': (13*"%s, ")[:-2]
        })
    values = tuple(v['entry'].get() for k, v in _widgets.items())
    # SQL command executing
    _cursor.execute(sql_command, values)
    # clearing FORM to next input

    cnx.commit()
    cnx.close()
    clear_all_inputs()


def clear_all_inputs():
    """Clear all Entry field values (empty texts)."""
    global _widgets
    for key in _widgets:
        _widgets[key]['entry'].delete(0, tk.END)


def f_delivery_point_add():
    """Process input FORM for new delivery point"""
    # -------------- main loop  -------------------------------------------------------------------
    root_frame = tk.Tk()

    root_frame.minsize(1000, 500)
    root_frame.title('PostMan. ')

    for i, key in enumerate(_widgets):
        _widgets[key]['label'] = ttk.Label(root_frame, text=_widgets[key]['text'],
                                           font=("Arial", 12))
        _widgets[key]['label'].grid(row=i, column=0, sticky=tk.W, padx=12)

        _widgets[key]['entry'] = ttk.Entry(root_frame, width=30)
        _widgets[key]['entry'].grid(row=i, column=1, pady=2, padx=20)

    submit_btn = ttk.Button(root_frame, text='Додати поля до бази', command=add_point_to_DB)
    submit_btn.grid(row=i+1, column=0, pady=10, padx=10, ipadx=40)

    clear_btn = ttk.Button(root_frame, text='Очистити всі поля', command=clear_all_inputs)
    clear_btn.grid(row=i+1, column=1, pady=10, padx=10, ipadx=40)

    root_frame.mainloop()


def f_delivery_point_edit():
    root_frame = tk.Tk()

    root_frame.minsize(1000, 500)
    root_frame.title('PostMan. ')

    for i, key in enumerate(_widgets):
        _widgets[key]['label'] = ttk.Label(root_frame, text=_widgets[key]['text'],
                                           font=("Arial", 12))
        _widgets[key]['label'].grid(row=i, column=0, sticky=tk.W, padx=12)

        _widgets[key]['entry'] = ttk.Entry(root_frame, width=30)
        _widgets[key]['entry'].grid(row=i, column=1, pady=2, padx=20)

    submit_btn = ttk.Button(root_frame, text='Додати поля до бази', command=add_point_to_DB)
    submit_btn.grid(row=i+1, column=0, pady=10, padx=10, ipadx=40)

    clear_btn = ttk.Button(root_frame, text='Очистити всі поля', command=clear_all_inputs)
    clear_btn.grid(row=i+1, column=1, pady=10, padx=10, ipadx=40)

    root_frame.mainloop()


def store_single_street_id():
    global root_frame
    root_frame.destroy()
    root_frame.quit()


def f_delivery_point_street_choice(point_params, streets_list):
    global _widgets, state_params
    global root_frame

    def processing(state_params, selected_data_row):
        state_params['selected_street']['id_street'] = selected_data_row.split('|')[-1]
        state_params['selected_street']['name'] = selected_data_row.split('|')[1]

    root_frame = tk.Tk()

    root_frame.minsize(1000, 500)
    root_frame.title('PostMan. ')

    for i, key in enumerate(_widgets):
        _widgets[key]['label'] = ttk.Label(root_frame, text=_widgets[key]['text'],
                                           font=("Arial", 12))
        _widgets[key]['label'].grid(row=i, column=0, sticky=tk.W, padx=12)

        _widgets[key]['entry'] = ttk.Entry(root_frame, width=30)
        _widgets[key]['entry'].grid(row=i, column=1, pady=2, padx=20)

    submit_btn = ttk.Button(root_frame, text='Зберігти обране', command=store_single_street_id)
    submit_btn.grid(row=i+1, column=0, pady=10, padx=10, ipadx=40)

    clear_btn = ttk.Button(root_frame, text='Очистити всі поля', command=clear_all_inputs)
    clear_btn.grid(row=i+1, column=1, pady=10, padx=10, ipadx=40)
    # TODO: finish it
    lbl_address_id = ttk.Label(root_frame, text='AddrID', font=("Arial", 12))
    lbl_address_id.grid(row=i+2, column=0, sticky=tk.W, padx=12)
    ent_address_id = ttk.Entry(root_frame, width=30)
    ent_address_id.grid(row=i+2, column=1, pady=2, padx=20)
    ent_address_id.insert(0, point_params["AddressID"])

    lbl_new_street_name = ttk.Label(root_frame, text='picked_street_name', font=("Arial", 12))
    lbl_new_street_name.grid(row=i+3, column=0, sticky=tk.W, padx=12)
    # TODO: finish it
    surname, name, middle_name = ФИО_to_surname_name_middlename(point_params["ФИО"])
    _widgets['surname']['entry'].insert(0, surname)
    _widgets['middle_name']['entry'].insert(0, middle_name)
    _widgets['name']['entry'].insert(0, name)

    _widgets['phone']['entry'].insert(0, point_params["телефон"])
    _widgets['city']['entry'].insert(0, point_params["город"])
    _widgets['street']['entry'].insert(0, point_params["улица"])
    _widgets['building']['entry'].insert(0, point_params["дом"])
    _widgets['floor']['entry'].insert(0, point_params["этаж"])
    _widgets['flat']['entry'].insert(0, point_params["квартира"])
    _widgets['comment']['entry'].insert(0, "")
    _widgets['branch']['entry'].insert(0, "")
    _widgets['post_ZIP']['entry'].insert(0, point_params["zipCode"])

    f_combobox_select(
        geometry='1000x618',
        combo_list_values=streets_list,
        select_field_width=70,
        save_quit_processing=processing,
    )

    print(state_params['selected_street']['id_street'], state_params['selected_street']['name'])

    ent_address_id.delete(0, tk.END)
    ent_address_id.insert(0, state_params['selected_street']['id_street'])

    lbl_new_street_name.config(
        text=('picked_street_name' + ':  ' + state_params['selected_street']['name'])
    )

    root_frame.focus_force()
    root_frame.mainloop()
