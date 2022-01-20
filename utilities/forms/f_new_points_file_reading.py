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

import winsound

from utilities.data_processing import addresses_processing, receive_addressIDs_by_api
from utilities.forms.f_delivery_points import f_delivery_point_street_choice
from utilities.utils import ФИО_to_surname_name_middlename
# from utilities.forms.f_combobox_select import f_combobox_select

import ua_posts_api
from settings import state_params

from model import (
    add_row_to_handbook_nd_get_added_id,
    get_if_street_building_surname_combo_id,
    add_row_values_to_DB,
)

global select_root

# TODO: rework this file to items reading


def save_addrs_to_DB(id_companies, id_postservices, df_addrs):
    """Save address to data base - table 'receivers'

    when address saving - have to sdo mirror saving  to table 'receiver_postcervice_street'
    To do it in next steps:
        0. Take from df_addrs row values for 'CityID', 'AddressID'
        1. Try to add City code to table 'Cities' and get the Citie's token table id
        2. Try to add Street code to table 'Streets' and get the Street's token table id
        3. Try to add new row to 'receiver_postcervice_street'
    """

    from datetime import date

    fields_list = ['id_companies', 'surname', 'name', 'middle_name',
                   'phone', 'city', 'street', 'building', 'floor', 'flat', 'comment',
                   'date_in', 'branch', 'is_active', 'post_ZIP']

    # fields = ", ".join(fields_list)
    """
    `id_receivers`, `id_companies`, `surname`, `name`, `middle_name`,
    `phone`, `city`, `street`, `building`, `floor`, `flat`, `comment`,
    `date_in`, `branch`, `is_active`, `post_ZIP`
    """
    # list_of_records = list()
    for row in df_addrs.itertuples():
        surname, name, middle_name = ФИО_to_surname_name_middlename(row.ФИО)
        new_point_row = (
            id_companies,
            surname, name, middle_name,
            row.телефон, row.город, row.улица, row.дом, int(row.этаж), row.квартира, "",
            date.today(), "", 1, row.zipCode
        )
        # step 0: Get from df_addrs row values for 'CityID', 'AddressID' - tokens for saving
        # city_token, street_token = row.CityID, row.AddressID
        # step 1: Try to add City code to table 'Cities' and get the Citie's token table id
        city_table_id = add_row_to_handbook_nd_get_added_id(
            handbook_id=dict(name='id_cities', value=None),
            filter_id=dict(name='postservice_id', value=id_postservices),
            token=dict(name='city_token', value=row.CityID),
            handbook_field=dict(name='city_name', value=row.post_city_name),  # was 'row.город'
            table_in='cities')
        # step 2. Try to add Street code to table 'Streets' and get the Street's token table id
        street_table_id = add_row_to_handbook_nd_get_added_id(
            handbook_id=dict(name='id_streets', value=None),
            filter_id=dict(name='city_id', value=city_table_id),
            token=dict(name='street_token', value=row.AddressID),
            handbook_field=dict(name='street_name',
                                value=row.post_street_name),   # was 'row.улица'
            table_in='streets')
        # step 3. Try to add new row to 'receiver_postcervice_street'
        receiver_id = get_if_street_building_surname_combo_id(
            rps_receivers_id=None,
            rps_postservices_id=id_postservices,
            rps_streets_id=street_table_id,
            building_to_check=row.дом,
            name_to_check=surname,
        )
        if not receiver_id and street_table_id:
            # add new receivers and get last_id
            work_d = dict(zip(fields_list, new_point_row))
            receiver_id = add_row_values_to_DB(
                'receivers',
                work_d
            )
        # add new (mirror) receivers for current postcervice_id
            print(
                F"receiver_id={receiver_id}, id_postservices={id_postservices} street_table_id={street_table_id}")
            _ = add_row_values_to_DB(
                'receiver_postservice_street',
                {
                    'rps_receivers_id': receiver_id,
                    'rps_postservices_id': id_postservices,
                    'rps_streets_id': street_table_id,
                }
            )
        df_addrs.at[row.Index, 'N'] = receiver_id
    return df_addrs


def select_file():
    global select_root

    filetypes = (
        ('*.xlsx файли тільки', '*.xlsx'),
        ('Будь-які файли', '*.*')
    )

    filename = askopenfilename(
        title='Виберіть файл з адресами',
        initialdir='.\\IN_DATA',
        filetypes=filetypes)

    showinfo(
        title='Вибрано файл:',
        message=filename
    )
    select_root.destroy()
    select_root.quit()
    return filename


def unclear_addrs_resolving(df_addrs: pd.DataFrame):
    import json
    # print(df_addrs.CityID)
    # df["Semester_Start"] = df["Semester"].apply(lambda x: str(x)[:3])

    for addr_key, addr_row in df_addrs[
            df_addrs.AddressID.apply(lambda x: str(x).startswith('[{'))].iterrows():
        # street_variants = json.loads(addr_row.AddressID)
        '''
        pprint(addr_row.AddressID)
        [{'Localization': 'UA',
          'addressDescr': {'descrEN': 'Poltavskyi Shliakhst.',
                           'descrLoc': 'вул.Полтавський Шлях',
                           'descrRU': 'ул.Полтавский Путь',
                           'descrUA': 'вул.Полтавський Шлях'},
          'addressID': 'a14aca8d-e0d4-11df-9b37-00215aee3ebe',
          'cityDescr': {'descrEN': 'Kharkiv',
                        'descrLoc': 'Харків',
                        'descrRU': 'Харьков',
                        'descrUA': 'Харків'},
          'cityID': '87162365-749b-11df-b112-00215aee3ebe',
          'latitude': 49.985756,
          'latitude_city': 49.992167,
          'longitude': 36.193311,
          'longitude_city': 36.231202,
          'newStringSearch_test': '%Полтавський%шлях%'},
         {'Localization': 'UA',
          'addressDescr': {'descrEN': 'Poltavskyi Shliakh',
                           'descrLoc': 'пров.Полтавський Шлях',
                           'descrRU': 'переулок Полтавский Путь',
                           'descrUA': 'пров.Полтавський Шлях'},
          'addressID': 'f0c34838-eda2-11df-b61a-00215aee3ebe',
          'cityDescr': {'descrEN': 'Kharkiv',
                        'descrLoc': 'Харків',
                        'descrRU': 'Харьков',
                        'descrUA': 'Харків'},
          'cityID': '87162365-749b-11df-b112-00215aee3ebe',
          'latitude': 49.985756,
          'latitude_city': 49.992167,
          'longitude': 36.193311,
          'longitude_city': 36.231202,
          'newStringSearch_test': '%Полтавський%шлях%'}]
        '''

        # variants = variants[variants.AddressID.apply(lambda x: x[0:2] == '[{')]
        # variants.AddressID = variants.AddressID.apply(lambda x: json.loads(x.replace("'", '"')))

        street_list_for_combolist = list()
        for el in addr_row.AddressID:
            # el_dict = json.loads(el)
            street_list_for_combolist.append(r"|".join(
                [el['cityDescr']['descrUA'],
                 el['addressDescr']['descrUA'],
                 el['addressID']
                 ])
            )

        pprint(addr_row.AddressID)
        f_delivery_point_street_choice(addr_row, street_list_for_combolist)

        df_addrs.at[addr_key, 'AddressID'] = state_params['selected_street']['id_street']
        df_addrs.at[addr_key, 'post_street_name'] = state_params['selected_street']['name']


def f_new_points_file_reading(postman, state_pars: dict):
    global select_root
    select_root = tk.Tk()
    select_root.title('Tkinter Open File Dialog')
    select_root.resizable(False, False)
    select_root.geometry('300x150')

    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    # get the file name
    xlsx_file_name = select_file()
    print(F'xlsx_file_name {xlsx_file_name}')

    # read the file
    if xlsx_file_name and xlsx_file_name.endswith('.xlsx'):

        # save current status bar StringVar for futher restoring
        status_text_is = state_pars['statusbar'].get()
        state_pars['statusbar'].set(status_text_is + '... почекайте  ...')

        df_addrs = addresses_processing(xlsx_file_name)

        df_addrs = receive_addressIDs_by_api(postman, df_addrs)
        # restore old status text:
        state_pars['statusbar'].set(status_text_is)

        unclear_addrs_resolving(df_addrs)

        df_addrs.to_excel('_'.join(['zipCodes', state_pars['client']['name'], '.xlsx']),
                          engine='xlsxwriter')

    # save data into the DB
    df_addrs = save_addrs_to_DB(
        state_params['client']['id_companies'],
        state_params['post_service']['id_postcervices'],
        df_addrs)
    df_addrs.to_excel('_'.join(['zipCodes', state_pars['client']['name'], 'with_ids', '.xlsx']),
                      engine='xlsxwriter')

    select_root.mainloop()


if __name__ == "__main__":
    from settings import credentials
    postman = ua_posts_api.Postman(credentials['Meest'])
    f_new_points_file_reading(postman, state_params)
