# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:18:38 2021

@author: manager
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

import pandas as pd

from pathlib import Path

import winsound

from utilities.data_processing import apointments_processing

import ua_posts_api
from settings import state_params

from model import (
    select_fields_from_table,
    add_row_values_to_DB,
    get_rps_id_by,
    get_items_id_by,
    add_row_to_waybills_nd_get_added_id,
)

global select_root


def sticker_text_by_name(name: str, items_in_parcel: int, items_total: int):
    return F"  {name}. \nВ упаковці {items_in_parcel}  шт. з {items_total} шт."


def calculate_weight_height_cost_volume1(
    item_weight: float, item_cost: float, high_x_100: float, length: float, width: float,
    packs_number: int,
    items_in_parcel: int,
):
    parcell_weight = round(item_weight * items_in_parcel, 2)
    parcell_height = int(items_in_parcel * high_x_100 / 100)
    parcell_cost = round(item_cost * items_in_parcel, 2)
    parcell_volume = parcell_height * length * width / 100 / 100 / 100  # metr 3
    return parcell_weight, parcell_height, parcell_cost, parcell_volume


def save_appointts_to_DB(df_appointts):  # TODO: rework SAVE FROM DF to DB
    """Save appointments to data base - table 'parcells'.  """

    """  # `parcells` DB fields list:

        SELECT `parcells`.`id_parcells`,
            `parcells`.`parcells_waybills_id`,
            `parcells`.`parcells_items_id`,
            `parcells`.`items_number`,
            `parcells`.`packs_number`,
            `parcells`.`weight_calculated`,
            `parcells`.`height_calculated`,
            `parcells`.`cost_calculated`,
            `parcells`.`pacells_pdf_file`,
            `parcells`.`text_to_sticker`
        FROM `postman`.`parcells`;

    """
    fields_list = [
        'parcells_waybills_id', 'parcells_items_id',
        'items_number', 'packs_number',
        'weight_calculated', 'height_calculated', 'parcell_volume_calculated', 'cost_calculated',
        'pacells_pdf_file', 'text_to_sticker'
    ]

    """  # the 'df_appointts' columns:
    names=['delivery_id', 'item_id_in_delivery', 'receivers_id'    #  was: 'addr_id',
           'parcels', 'items_total', 'items_in_parcel',
           'pdf_name'],
    """

    # list_of_records = list()
    for row in df_appointts.itertuples():

        rps_postservices_id = select_fields_from_table(
            fields='postservice_id',  # TODO: postcerviceS_id
            table='delivery_contracts',
            where_condition=F'is_active and id_delivery_contract = {row.delivery_id}'
        )[0][0]

        waybills_rps_id = get_rps_id_by(
            rps_postservices_id,
            row.receivers_id,
        )
        # step 1: Try to add new waybill to table 'contract_waybills' and get
        #         the waubills id id:
        waybills_id = add_row_to_waybills_nd_get_added_id(  # !!!!!  Тута 2022-01-17
            row.delivery_id,  # for get id if exists!
            row.receivers_id,
            to_insert={
                'delivery_contracts_id': row.delivery_id,
                'waybills_receivers_id': row.receivers_id,
                'waybills_rps_id': waybills_rps_id,
            },
        )

        items_id = get_items_id_by(row.delivery_id, row.item_id_in_delivery)

        # get_item_name_by(items_id, row)
        item_name = select_fields_from_table(
            table='items', fields='item_name',
            where_condition=F"id_items={items_id}"
        )[0][0]
        assert item_name, F"get_item_name_by(items_id) with id={items_id} returns nothing"

        text_to_sticker = sticker_text_by_name(item_name, row.items_in_parcel, row.items_total)

        (item_weight, item_cost, height_x_100, length, width) = select_fields_from_table(
            table='items',
            fields='item_weight, item_cost, height_x_100, length, width',
            where_condition=F"id_items={items_id}"
        )[0]

        parc_weight, parc_height, parc_cost, parc_volume = calculate_weight_height_cost_volume1(
            item_weight, item_cost, height_x_100, length, width, row.parcels, row.items_in_parcel
        )

        new_row = (
            waybills_id, items_id,      # 'parcells_waybills_id', 'parcells_items_id',
            row.items_total,            # 'items_number',
            row.parcels,                # 'packs_number',
            parc_weight,                # `weight_calculated`,
            parc_height,                # 'height_calculated',
            parc_volume,                # 'parcell_volume_calculated',
            parc_cost,                  # 'cost_calculated',
            row.pdf_name,               # 'pacells_pdf_file'
            text_to_sticker,            # text_to_sticker
        )

        work_d = dict(zip(fields_list, new_row))
        new_parcell_id = add_row_values_to_DB('parcells',  work_d)

        df_appointts.at[row.Index, 'N'] = new_parcell_id

    return df_appointts


def select_file():   # TODO: universal procrdure !!!
    global select_root

    filetypes = (
        ('*.xlsx файли тільки', '*.xlsx'),
        ('Будь-які файли', '*.*')
    )

    filename = askopenfilename(   # TODO: universal name substituition
        title='Виберіть файл з призначеннями продукції одержувачам:',
        initialdir='.\\IN_DATA',  # TODO: universal path substituition
        filetypes=filetypes)

    showinfo(
        title='Вибрано файл:',
        message=filename
    )
    select_root.destroy()
    select_root.quit()
    return filename


def f_new_items_appointts_file_reading(state_pars: dict):
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

        delivery_code_for_check, df_apointments = apointments_processing(xlsx_file_name)

        # restore old status text:
        state_pars['statusbar'].set(status_text_is)

        if delivery_code_for_check != state_params['delivery_contract']['id_delivery_contract']:
            print("НЕ ТОЙ КОД ПОСТАВКИ!!")  # TODO:  give the tkinter message window here!!!
        else:
            # TODO: check items/receivers codes and save appointments to DB
            # save data into the DB
            df_apointments = save_appointts_to_DB(df_apointments)

            df_apointments.to_excel(
                '_'.join([xlsx_file_path.stem, state_pars['client']['name'], 'appoint', '.xlsx']),
                engine='xlsxwriter'
            )

    select_root.mainloop()


if __name__ == "__main__":
    from settings import credentials
    postman = ua_posts_api.Postman(credentials['Meest'])
    # f_new_points_file_reading(postman, state_params)
