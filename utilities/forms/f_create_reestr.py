# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:09:59 2022

@author: manager
"""
# =============================================================================
# import tkinter as tk
# from tkinter.filedialog import askopenfilename
# from tkinter.messagebox import showinfo
# =============================================================================

# from pathlib import Path
from tkinter.messagebox import showinfo

import winsound

from model import (
    select_fields_from_table,
    waybills_sum_filling,
    # add_row_values_to_DB,
    # get_items_id_by,
    create_parcels_by_api,
    update_many,
)


def f_create_reestr(postman, state_pars: dict):
    # TODO: message box with progress bar )
    #  calculate waybill's totals & save it in DB - table 'contract_waybills' in three steps:
    # step 1/3. Pick all parcells for each waybill from DB - table 'contract_waybills'
    # curr_postservice = state_pars['post_service']['id_postcervices']
    curr_contract_id = state_pars['delivery_contract']['id_delivery_contract']

    # =============================================================================
    # def select_fields_from_table(
    #         fields='id, company_name, short_name_latin',
    #         table='companies',
    #         where_condition='is_active'
    # ):
    # =============================================================================

    '''
    SELECT `contract_waybills`.`id_waybills`,
        `contract_waybills`.`delivery_contracts_id`,
        `contract_waybills`.`waybills_receivers_id`,
        `contract_waybills`.`waybills_rps_id`,
        `contract_waybills`.`total_cost`,
        `contract_waybills`.`total_volume`,
        `contract_waybills`.`total_weight`,
        `contract_waybills`.`total_places`,
        `contract_waybills`.`contract_waybills_token`,
        `contract_waybills`.`waybils_pdf_file_name`
    FROM `postman`.`contract_waybills`;



    SELECT `delivery_contracts`.`id_delivery_contract`,
        `delivery_contracts`.`postservice_id`,
        `delivery_contracts`.`id_companies`,
        `delivery_contracts`.`name`,
        `delivery_contracts`.`bank_account`,
        `delivery_contracts`.`subcontract_nnumber`,
        `delivery_contracts`.`sending_date`,
        `delivery_contracts`.`payer`,
        `delivery_contracts`.`finished`,
        `delivery_contracts`.`is_active`
    FROM `postman`.`delivery_contracts`;

    '''

    tokens_for_reestr = select_fields_from_table(
        fields='contract_waybills_token',
        table='contract_waybills',
        where_condition=F'delivery_contracts_id={curr_contract_id}'
    )
    tokens_list = [token[0] for token in tokens_for_reestr]

    sending_date = select_fields_from_table(
        fields='sending_date',
        table='delivery_contracts',
        where_condition=F'id_delivery_contract={curr_contract_id}'
    )[0][0]

    expected_pick_date = dict(
        date=sending_date.strftime("%d.%m.%Y"),  # "20.01.2022"
        timeFrom="15:00",
        timeTo="18:00"),

    postman.register.create_pick_up(
        expected_pick_date=expected_pick_date,
        parcels_tokens_list=tokens_list
    )

    showinfo(
        title='Створення реєстру Заверщено:',
        message=F"Додано {len(tokens_list)} ЕН"
    )
