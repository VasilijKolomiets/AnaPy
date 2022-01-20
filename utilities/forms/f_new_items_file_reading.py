# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:18:38 2021

@author: manager
"""
from pprint import pprint

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

import pandas as pd

from pathlib import Path

import winsound

from utilities.data_processing import items_processing

import ua_posts_api
from settings import state_params

from model import (
    add_row_values_to_DB,
)

global select_root

# TODO: rework this file to items reading


def save_items_to_DB(df_items):
    """Save items to data base - table 'items'.  """

    fields_list = [  # TODO: using zip ???
        'delivery_contracts_id', 'item_id_in_delivery', 'item_name',
        'item_weight', 'item_cost',
        'length', 'width', 'height_x_100'
    ]

    """  # 'items' DB fields list:
    `id_items`, `delivery_contracts_id`,  `item_id_in_delivery`,  `item_name`,
    `item_weight`, `item_cost`,
    `length`, `width`, `height_x_100`
    """
    # list_of_records = list()
    for row in df_items.itertuples():
        new_item_id = add_row_values_to_DB(
            'items',
            {
                'delivery_contracts_id': row.код_поставки,
                'item_id_in_delivery': row.item_id,
                'item_name': row.наименование_изделия,
                'item_weight': row.weight_1,
                'item_cost': row.value_1,
                'length': row.length,
                'width': row.width,
                'height_x_100': row.height_x_100
            }
        )
        df_items.at[row.Index, 'N'] = new_item_id

    return df_items


def select_file():   # TODO: universal procrdure !!!
    global select_root

    filetypes = (
        ('*.xlsx файли тільки', '*.xlsx'),
        ('Будь-які файли', '*.*')
    )

    filename = askopenfilename(
        title='Виберіть файл з продукцією:',  # TODO: universal name substituition
        initialdir='.\\IN_DATA',              # TODO: universal path substituition
        filetypes=filetypes)

    showinfo(
        title='Вибрано файл:',
        message=filename
    )
    select_root.destroy()
    select_root.quit()
    return filename


def f_new_items_file_reading(state_pars: dict):
    global select_root
    select_root = tk.Tk()
    select_root.title('Tkinter Open File Dialog')
    select_root.resizable(False, False)
    select_root.geometry('300x150')

    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    # get the file name
    xlsx_file_name = select_file()    # TODO: universal procrdure !!!
    xlsx_file_path = Path(xlsx_file_name)
    print(F'xlsx_file_name {xlsx_file_name}')

    # read the file
    if xlsx_file_name and xlsx_file_name.endswith('.xlsx'):

        # save current status bar StringVar for futher restoring
        status_text_is = state_pars['statusbar'].get()
        state_pars['statusbar'].set(status_text_is + '... почекайте  ...')

        delivery_code_for_check, df_items = items_processing(xlsx_file_name)

        # restore old status text:
        state_pars['statusbar'].set(status_text_is)

        if delivery_code_for_check != state_params['delivery_contract']['id_delivery_contract']:
            print("НЕ ТОЙ КОД ПОСТАВКИ!!")  # TODO:  give the tkinter message window here!!!
        else:
            # save data into the DB
            df_items = save_items_to_DB(df_items)

            df_items.to_excel(
                '_'.join([xlsx_file_path.stem, state_pars['client']['name'], '.xlsx']),
                engine='xlsxwriter'
            )
            print("Імпорт завершено успішно!")     # TODO: message on top!
    select_root.mainloop()


if __name__ == "__main__":
    from settings import credentials
    postman = ua_posts_api.Postman(credentials['Meest'])
    # f_new_points_file_reading(postman, state_params)
