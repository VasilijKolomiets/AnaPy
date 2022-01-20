# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:15:56 2022

@author: manager
"""

from pathlib import Path

from PyPDF2 import PdfFileReader, PdfFileWriter
import base64

from utilities.utils import txt_to_image_EN, image_to_pdf

from model import select_fields_from_table, update_many, get_ordered_parcells_by_waybill


def work_out_pdf_name(firm_name, delivery_firm, waybill_id):
    return "_".join([firm_name, delivery_firm, str(waybill_id), '.pdf'])


def group_stickers_into_pdfs(curr_contracts_id,
                             subfolder_to_read_from: str = '_work_pdf',
                             folder_to_write_in: str = '_resulting_pdfs',
                             ):

    here_path = Path('.').resolve()   # .parent

    contract_waybills = select_fields_from_table(
        fields=' id_waybills, waybils_pdf_file_name ',
        table='contract_waybills',
        where_condition=F'contract_waybills.delivery_contracts_id = {curr_contracts_id}'
    )

    for waybill_id, waybils_pdf_file_name in contract_waybills:

        pdf_path = here_path / subfolder_to_read_from / waybils_pdf_file_name
        input_pdf = PdfFileReader(str(pdf_path.absolute()))

        # get waybill's parcells info:
        waybill_parcells = get_ordered_parcells_by_waybill(waybill_id)
        # pages_quants_to_split
        page_start, page_end_1 = 0, 0
        for parcel_info in waybill_parcells:
            pdf_writer = PdfFileWriter()
            # `parcells`:  packs_number, pacells_pdf_file:
            pages_quantity, parcel_file_prefix = parcel_info[4], parcel_info[-2]

            page_end_1 += pages_quantity
            for k in range(page_start, page_end_1):
                page = input_pdf.getPage(k)
                pdf_writer.addPage(page)
            page_start = page_end_1

            with (here_path / folder_to_write_in / '_'.join(
                    ['printme', parcel_file_prefix, waybils_pdf_file_name])
                  ).open(mode="wb") as output_file:
                pdf_writer.write(output_file)


def subscribe_pdfs_stickers(df_common,
                            firm_name: str = 'oschad', delivery_firm: str = 'meest',
                            subfolder_to_read_from: str = '_resulting_pdfs',
                            ):
    # , text_to_sticker
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


def f_create_waybills_pdf(postman, state_pars: dict,
                          folder_path: str = '_work_pdf',
                          ):

    path_to_save = Path('.').resolve() / folder_path  # .parent
    curr_contracts_id = state_pars['delivery_contract']['id_delivery_contract']

    """
    SELECT
        short_name_latin, postservice_name
    FROM
        delivery_contracts t1
            JOIN
        companies t2 ON t1.id_companies = t2.id
            JOIN
        postservices t3 ON t1.postservice_id = t3.id_postcervices
    WHERE
        id_delivery_contract = 1;
    """
    short_name_latin, postservice_name = select_fields_from_table(  # TODO: CRUD
        fields=' short_name_latin, postservice_name ',
        table=""" delivery_contracts t1
                JOIN
                    companies t2 ON t1.id_companies = t2.id
                JOIN
                    postservices t3 ON t1.postservice_id = t3.id_postcervices
        """,
        where_condition=F' id_delivery_contract = {curr_contracts_id}'
    )[0]

    # get waybills id list and create waybills file_name and save its in DB in two steps
    contract_waybills = select_fields_from_table(
        fields=' id_waybills ',
        table='contract_waybills',
        where_condition=F'contract_waybills.delivery_contracts_id = {curr_contracts_id}'
    )
    # step 1/2. Create waybills file_name.
    filenames_list = [
        (work_out_pdf_name(short_name_latin, postservice_name,  waybill_id[0]), waybill_id[0])
        for waybill_id in contract_waybills
    ]
    # step 2/2/ Save waybills file_name into DB:
    update_many(tablename='contract_waybills',
                fields_name=['waybils_pdf_file_name', 'id_waybills'],
                values=filenames_list)

    waybills_for_contract = select_fields_from_table(
        fields='id_waybills, contract_waybills_token, waybils_pdf_file_name ',
        table='contract_waybills',
        where_condition=F'contract_waybills.delivery_contracts_id = {curr_contracts_id}'
    )

    for id_waybills, contract_waybills_token, waybils_pdf_file_name in waybills_for_contract:
        code, pdf_bytes = postman.to_print.sticker100(parcels_IDs_list=[contract_waybills_token, ])
        if code == 200:
            with open(path_to_save / waybils_pdf_file_name, 'wb') as f:
                # f.write(base64.b64decode(pdf_bytes))
                f.write(pdf_bytes)

    group_stickers_into_pdfs(curr_contracts_id)
