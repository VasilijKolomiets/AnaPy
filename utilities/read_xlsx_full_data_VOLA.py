# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:11:46 2021

№	ID	город	улица	дом	кв	этаж	ФИО	Номер телефона

"""
import time
from pathlib import Path

import pandas as pd
import numpy as np

import json

from PyPDF2 import PdfFileReader, PdfFileWriter
import base64

import utils
import ua_posts_api


# TODO: totalone box weight / height / value
# contents_items_forming - subdictionary for each common sending


def addresses_processing(path_ro_xlsx: Path, sheet_name='АП'):
    """Process the addresses table."""
    df_addrs = pd.read_excel(path_ro_xlsx, sheet_name=sheet_name,
                             header=1,
                             usecols=list(range(11)),
                             dtype=dict(N=int,
                                        addr_id=int,
                                        город=str,
                                        улица=str,
                                        дом=str,
                                        квартира=str,
                                        этаж=int,
                                        ФИО=str,
                                        телефон=str,
                                        zipCode=str,
                                        ),
                             # skiprows=0,
                             )  # .dropna()

    df_addrs.город = df_addrs.город.str.replace("'", "`", regex=False)
    df_addrs.улица = df_addrs.улица.str.replace("'", "`", regex=False)
    df_addrs.улица = df_addrs.улица.str.replace(")", " ", regex=False)
    df_addrs.улица = df_addrs.улица.str.replace("(", " ", regex=False)

    return df_addrs


def receive_addressIDs_by_api(postman: ua_posts_api.Postman(), df_addrs):
    # =============================================================================
    # # addressID (ID for street in City) receiving
    # =============================================================================
    df_addrs.loc[:, ['CityID', 'AddressID', 'parcelID', 'itemsID_list']] = ''

    for index, row in df_addrs.iterrows():
        # CityID by zipCode   # TODO: before merge!!! do it
        print(index, "\n", row, "\n")
        if row.zipCode is np.nan:
            continue

        code, response_ = postman.search.by_zip_city_id(zipCode=row.zipCode)
        city_ids = postman._city_by_ZIP_wise_pick(response_,
                                                  city_name=row.город, zipCode=row.zipCode)
        print(F'city_ids============{city_ids}')
        df_addrs.at[index, 'CityID'] = city_ids

        # AddressID by CityID
        code, response = postman.search.address_id(city_id=city_ids, streetname=row.улица)

        if len(response) == 1:
            print(row.город, row.zipCode, 'resp code=', code, response[0]['addressID'], "--Ok--")
            df_addrs.at[index, 'AddressID'] = response[0]['addressID']
        else:
            print(row.город, row.zipCode, 'resp code=', code, response)
            df_addrs.at[index, 'AddressID'] = response

    return df_addrs


def items_processing(path_ro_xlsx: Path, sheet_name='Код_Прод'):
    """Proces the items table."""
    df_items = pd.read_excel(path_ro_xlsx, sheet_name=sheet_name,
                             header=0,
                             usecols=[0, 2, 4, 5, 6, 7, 8],
                             dtype=dict(
                                 вес=float,
                             )
                             # skiprows=0,
                             )  # .dropna()
    return df_items


def apointments_processing(path_ro_xlsx: Path, sheet_name='ALL_Адрес'):
    """Process the apointments table."""
    df_apointments = pd.read_excel(path_ro_xlsx, sheet_name=sheet_name,
                                   header=None,
                                   usecols=[1, 2, 3, 4, 5],
                                   # skiprows=0,
                                   names=['item_id', 'addr_id',
                                          'parcels', 'items_total', 'items_in_parcel', ],
                                   dtype=dict(
                                       items_in_parcel=float),
                                   )  # .dropna() how='all'

    df_apointments.items_in_parcel = df_apointments.items_total / df_apointments.parcels
    # TODO: DRY
    df_apointments.items_in_parcel.replace('nan', np.nan, inplace=True)
    df_apointments.dropna(subset=['items_in_parcel', ], inplace=True)

    # pdf file name for each sticker saving
    df_apointments.loc[:, 'pdf_name'] = (df_apointments.item_id.astype(str) + '_'
                                         + df_apointments.addr_id.astype(str) + '_'
                                         + df_apointments.parcels.astype(str) + '_'
                                         + df_apointments.items_total.astype(str)
                                         + '.pdf'
                                         )

    return df_apointments


def create_common_table(df_addrs, df_items, df_apointments):
    """Process the apointments table."""
    df_common = df_addrs.join(df_apointments.set_index('addr_id'),
                              on='addr_id', how='right'
                              ).join(df_items.set_index('item_id'),
                                     on='item_id', how='left'
                                     )

    # =============================================================================
    df_common.loc[:, 'text_to_sticker'] = (
        df_common.Изделие + '\n В упаковці ' + df_common.items_in_parcel.astype(str) + ' шт. з '
        + df_common.items_total.astype(str) + ' шт.')

    df_common.loc[:, 'a_weight'] = (df_common.вес * df_common.items_in_parcel).round(2)
    df_common.loc[:, 'a_height'] = (df_common.height_x_100 / 100 * df_common.items_in_parcel
                                    ).round(2)
    df_common.loc[:, 'a_value'] = (df_common.value_1 * df_common.items_in_parcel
                                   ).fillna(0).round(2)
    # =============================================================================

    return df_common


def create_parcels_by_api(postman: ua_posts_api.Postman(), df_addrs, df_common):
    """Create parcels using api. First form dicts needed."""
# =============================================================================
#     df_common.columns.to_list()
#         ['№',
#          'addr_id',
#          'город',
#          'улица',
#          'дом',
#          'квартира',
#          'этаж',
#          'ФИО',
#          'телефон',
#          'zipCode',
#          'CityID',
#          'AddressID',
#          'item_id',
#          'parcels',
#          'items_total',
#          'items_in_parcel',
#          'pdf_name',
#          'Изделие',
#          'вес',
#          'файл',
#          'value_1',
#          'length',
#          'width',
#          'height_x_100',
#          'text_to_sticker',
#          'a_weight',
#          'a_height',
#          'a_value']
# =============================================================================
    """
                json={
                    "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
                    "receiverPay": False,
                    # "COD": 600,
                    "notation": ".......",
                    "sender": {
                       "phone": kwargs.get('sender_phone', "+38050-421-1558"),
                       "name": kwargs.get('sender_name', 'Васина Лариса'),
                       },
                    "placesItems": [  # TODO:  form and gives dictionary here &&?
                        {"weight": kwargs['weight'],                        # 1
                         "height": kwargs.get('height', 0.01),                 # 2
                         "width":  kwargs.get('width', 0.01),                  # 3
                         "length": kwargs.get('length', 0.01),                 # 4
                         "insurance": kwargs.get('insurance', 500),
                         "quantity": kwargs.get('quantity', 1),             # 16
                         }
                    ],
                    'contentsItems': [   # TODO:  form and gives dictionary here &&?
                        {
                            'contentName': kwargs['contentName'],           # 6
                            'quantity':	1,
                            'weight': 0.101,                                # 7
                            'value': 0.362,                                 # 8
                        },
                    ],
                    "receiver": {  # TODO:  form and gives dictionary here &&?
                        "name": kwargs['name'],                                # 9
                        "phone": kwargs['phone'],                              # 10
                        "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",
                        "zipCode": kwargs['zipCode'],                          # 11
                        "addressID": kwargs['addreeID'],                       # 12
                        "building": kwargs['building'],                        # 13
                        "flat": kwargs.get('flat', "1"),
                        "floor": kwargs.get('floor', 1),                       #15
                        "service": "Door",
                    },

                    "payType": "noncash",
                }
            )
            self.auth_response_code = response.status_code
            content_result = json.loads(response.content)['result']
            return response.status_code, content_result
    """
    # TODO: DRY
    df_common.вес.replace('nan', np.nan, inplace=True)
    df_common.dropna(subset=['вес', ], inplace=True)

    df_addrs.этаж.replace('nan', np.nan, inplace=True)
    df_addrs.квартира.replace('nan', np.nan, inplace=True)
    df_addrs.квартира.replace('nan', np.nan, inplace=True)

    # for each addr filter rows with diff item sending
    for s_key, sending in df_addrs.iterrows():

        kwargs = dict(placesItems=[], receiver=None)
        itemsID_list = list()  # for conseq added items quantities saving
        for key, item in df_common.query("addr_id == @sending.addr_id").iterrows():

            itemsID_list.append({item.item_id: item.parcels})

            kwargs["placesItems"].append({
                "weight": round(item.a_weight, 3),
                # "height": 5,
                # "width":  4,
                # "length": 7,
                "insurance": round(item.a_value, 2),
                "quantity": item.parcels,
            })
            #    sum total w8
            #    find max sizes

        #    create sending description
        kwargs["receiver"] = {
            "name": sending.ФИО,
            "phone": sending.телефон,
            "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",

            "addressID": sending.AddressID,
            "building": sending.дом,
            "service": "Door",
        }
        if sending.zipCode is not np.nan:
            kwargs["receiver"]["zipCode"]: sending.zipCode
        if sending.этаж is not np.nan:
            kwargs["receiver"]["floor"] = int(sending.этаж)
        if sending.квартира is not np.nan:
            kwargs["receiver"]["flat"] = sending.квартира

        print("\n", kwargs)
        #
        #    create parcel with api
        #
        resp_code, result = postman.parcels.create(**kwargs)
        #
        #    change addr_common
        #
        # parcelID
        print(resp_code, result)

        df_addrs.at[s_key, 'itemsID_list'] = json.dumps(itemsID_list)

        if resp_code == 200 and 'parcelID' in result:
            df_addrs.at[s_key, 'parcelID'] = result['parcelID']

    df_addrs.parcelID.replace('nan', np.nan, inplace=True)

    return df_addrs


def work_out_pdf_name(firm_name, parcelID, delivery_firm):
    return "_".join([firm_name, parcelID, delivery_firm, '.pdf'])


def get_stickers_by_api(postman: ua_posts_api.Postman(), df_addr,
                        firm_name: str = 'oschad', delivery_firm: str = 'meest',
                        subfolder_to_save_in: str = '_work_pdf',
                        ):

    folder_path = Path('.').resolve().parent / subfolder_to_save_in
    for key, row in df_addr.iterrows():
        if not row.AddressID or row.parcelID is np.nan:
            continue

        # print(F'row.parcelID for print.sticker100 ------>{row.parcelID}')
        code, pdf_bytes = postman.print.sticker100(parcels_IDs_list=[row.parcelID, ])
        if code == 200:
            with open(folder_path / work_out_pdf_name(firm_name, row.parcelID, delivery_firm),
                      'wb') as f:
                # f.write(base64.b64decode(pdf_bytes))
                f.write(pdf_bytes)


def group_stickers_into_pdfs(df_addrs,
                             firm_name: str = 'oschad', delivery_firm: str = 'meest',
                             subfolder_to_read_from: str = '_work_pdf',
                             folder_to_write_in: str = '_resulting_pdfs',
                             ):

    here_path = Path('.').resolve().parent

    for key, row in df_addrs.iterrows():

        if json.loads(row.itemsID_list) == [] or not row.parcelID:
            continue

        pdf_path = here_path / '_work_pdf' / work_out_pdf_name(
            firm_name, row.parcelID, delivery_firm)
        input_pdf = PdfFileReader(str(pdf_path.absolute()))

        # like this:: 	itemsID_list"[{""4"": 1}, {""8"": 3}, {""11"": 1}]"
        itemsID_list = json.loads(row.itemsID_list)
        # pages_quants_to_split = [di.popitem()[1] for di in itemsID_list]  # take dicts value
        page_start, page_end_1 = 0, 0
        for items_dict in itemsID_list:
            item_id, pages_quantity = items_dict.popitem()
            pdf_writer = PdfFileWriter()

            page_end_1 += pages_quantity
            for k in range(page_start, page_end_1):
                page = input_pdf.getPage(k)
                pdf_writer.addPage(page)
            page_start = page_end_1

            with (here_path / folder_to_write_in / '_'.join(
                    ['deleteme', str(item_id), str(row.addr_id), '.pdf'])).open(
                    mode="wb") as output_file:
                pdf_writer.write(output_file)


def subscribe_pdfs_stickers(df_common,
                            firm_name: str = 'oschad', delivery_firm: str = 'meest',
                            subfolder_to_read_from: str = '_resulting_pdfs',
                            ):

    # take files '*.pdf' from folder
    here_path = Path('.').resolve().parent
    for pdf_file in (here_path / subfolder_to_read_from).iterdir():
        # pick item_id & addr_id from file name
        if pdf_file.suffix != ".pdf":
            continue
        item_id, addr_id = (int(el) for el in pdf_file.name.split('_')[1:3])
        # get text to print from df_commmon
        text_to_print = df_common.query(
            'item_id==@item_id and addr_id==@addr_id'
        ).text_to_sticker.values[0]
        # create image from text
        utils.txt_to_image_EN(text_to_print, pdf_file.with_suffix('.png'))
        # insert image with text pdf 'page' times in "right places"
        utils.image_to_pdf(pdf_filename=pdf_file, image_f_name=pdf_file.with_suffix('.png'))


if __name__ == '__main__':

    postman = ua_posts_api.Postman()
    file_name = r'GOOD_Пумб.xlsx'
    client_name = file_name[4:-5]
    path_ro_xlsx = Path(r"..\IN_DATA") / file_name

    df_addrs = addresses_processing(path_ro_xlsx)

    df_addrs = receive_addressIDs_by_api(postman, df_addrs)
    df_addrs.to_excel('zipCodes_'+client_name + '.xlsx', engine='xlsxwriter')

    df_items = items_processing(path_ro_xlsx)
    df_items.to_excel('items_' + client_name + str(time.time()).replace('.', '_')
                      + '.xlsx', engine='xlsxwriter')

    df_apointments = apointments_processing(path_ro_xlsx)

    df_common = create_common_table(df_addrs, df_items, df_apointments)
    df_common.to_excel('211212_' + client_name + '_grosstotal.xlsx', engine='xlsxwriter')

    df_addrs = create_parcels_by_api(postman, df_addrs, df_common)
    df_addrs.to_excel(('zipCodes_'+client_name + str(time.time()).replace('.', '_')
                       + '.xlsx'), engine='xlsxwriter')
    # TODO: repair it!
    df_common.drop('parcelID', axis=1, inplace=True)
    df_common = df_common.join(df_addrs[['addr_id', 'parcelID']].set_index('addr_id'),
                               on='addr_id')

    print('---------------------get_stickers_by_api')
    get_stickers_by_api(postman, df_common)

    print('---------------------group_stickers_into_pdfs')
    group_stickers_into_pdfs(df_addrs)

    print('---------------------subscribe_pdfs_stickers')
    subscribe_pdfs_stickers(df_common)
