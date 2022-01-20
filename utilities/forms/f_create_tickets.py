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

import winsound

from model import (
    # select_fields_from_table,
    waybills_sum_filling,
    # add_row_values_to_DB,
    # get_items_id_by,
    create_parcels_by_api,
    update_many,
)


def f_create_tickets(postman, state_pars: dict):
    # TODO: message box with progress bar )
    ...
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
    '''

    '''
    SELECT `parcells`.`id_parcells`,
        `parcells`.`parcells_waybills_id`,
        `parcells`.`parcells_items_id`,
        `parcells`.`items_number`,
        `parcells`.`packs_number`,
        `parcells`.`weight_calculated`,
        `parcells`.`height_calculated`,
        `parcells`.`cost_calculated`,
        `parcells`.`parcell_volume_calculated`,
        `parcells`.`pacells_pdf_file`,
        `parcells`.`text_to_sticker`
    FROM `postman`.`parcells`;
    '''

    # curr_waybills = select_fields_from_table(
    #     fields='*',
    #     table='contract_waybills',
    #     where_condition=F'delivery_contracts_id={curr_contract_id}'
    # )

    # step 2/3. Calculate waybill's totals
    """
    SELECT
        SUM(cost_calculated * packs_number) AS total_cost,
        SUM(weight_calculated * packs_number) AS total_weight,
        SUM(parcell_volume_calculated * packs_number) AS total_volume,
        SUM(packs_number) AS total_places
        parcells_waybills_id,
    FROM
        postman.parcells
    GROUP BY (parcells_waybills_id)
    WHERE parcells_waybills_id = id;
    """
    data_to_store = waybills_sum_filling(curr_contract_id)

    # step 3/3. Save waybill's totals into DB - table 'contract_waybills'
    update_many(
        tablename='contract_waybills',
        fields_name=[
            'total_cost', 'total_volume', 'total_weight', 'total_places',
            'id_waybills'
        ],
        values=data_to_store
    )

    #  create waybiils in postserice API
    create_parcels_by_api(postman, state_pars)
    # TODO: split save   create_parcels_by_api postservice's  waybiil's tokens into DB - table 'contract_waybills'
    # ??? now saving in  create_parcels_by_api - it is not good !!!
    print("tickets done...")
