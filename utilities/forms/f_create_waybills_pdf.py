# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:15:56 2022

@author: manager
"""
from pathlib import Path
from model import select_fields_from_table


def f_create_waybills_pdf(postman, state_pars: dict,
                          folder_path: str = '_work_pdf',
                          ):

    path_to_save = Path('.').resolve() / folder_path  # .parent
    curr_contracts_id = state_pars['delivery_contract']['id_delivery_contract']

    waybills_for_contract = select_fields_from_table(
        fields='id_waybills, contract_waybills_token, waybils_pdf_file_name ',
        table='contract_waybills',
        where_condition=F'contract_waybills.delivery_contracts_id = {curr_contracts_id}'
    )

    for id_waybills, contract_waybills_token, waybils_pdf_file_name in waybills_for_contract:
        code, pdf_bytes = postman.print.sticker100(parcels_IDs_list=[contract_waybills_token, ])
        if code == 200:
            with open(path_to_save / waybils_pdf_file_name, 'wb') as f:
                # f.write(base64.b64decode(pdf_bytes))
                f.write(pdf_bytes)


"""
    df_apointments.loc[:, 'pdf_name'] = (
        df_apointments.delivery_id.astype(str) + '_'
        + df_apointments.receivers_id.astype(str) + '_'
        + df_apointments.item_id_in_delivery.astype(str) + '_'
        + df_apointments.parcels.astype(str) + '_'
        + df_apointments.items_total.astype(str)
        + '.pdf'
    )
"""


def subscribe_pdfs_stickers(df_common,
                            firm_name: str = 'oschad', delivery_firm: str = 'meest',
                            subfolder_to_read_from: str = '_resulting_pdfs',
                            ):


def work_out_pdf_name(firm_name, parcelID, delivery_firm):
    return "_".join([firm_name, parcelID, delivery_firm, '.pdf'])
