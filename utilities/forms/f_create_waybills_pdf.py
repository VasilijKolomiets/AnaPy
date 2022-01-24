# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:15:56 2022

@author: manager
"""

from pathlib import Path

from PyPDF2 import PdfFileReader, PdfFileWriter
# import base64

from tkinter.messagebox import showinfo

import utilities.utils as utils

from model import select_fields_from_table, update_many, get_ordered_parcells_by_waybill


def work_out_pdf_name(firm_name, delivery_firm, waybill_id):
    return "_".join([firm_name, delivery_firm, str(waybill_id), '.pdf'])


def group_stickers_into_pdfs(curr_contracts_id,
                             subfolder_to_read_from: str = '_work_pdf',
                             folder_to_write_in: str = '_resulting_pdfs',
                             ):
    # read more heare: https://realpython.com/pdf-python/
    # https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
    #
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


def subscribe_pdfs_stickers(curr_contracts_id,
                            subfolder_to_read_from: str = '_resulting_pdfs',
                            ):

    # take files '*.pdf' from folder
    here_path = Path('.').resolve()  # .parent
    for pdf_file in (here_path / subfolder_to_read_from).iterdir():

        if pdf_file.suffix != ".pdf":
            continue
        if int(pdf_file.name.split('_')[1]) != curr_contracts_id:
            continue

        # pick item_id & addr_id from file name
        # take '1_2_22.0_3_66_366' from 'printme_1_2_22.0_3_66_366__pumb_Meest_83_':
        search_text = "_".join(pdf_file.name.split('_')[1:7])
        # get text to print from 'patcels' table:
        text_to_print = select_fields_from_table(
            fields=' text_to_sticker ',
            table='parcells',

            where_condition=F"""INSTR(pacells_pdf_file, '{search_text}') > 0"""

        )[0][0]
        # create image from text
        utils.txt_to_image_EN(text_to_print, pdf_file.with_suffix('.png'))
        # insert image with text pdf 'page' times in "right places"
        utils.image_to_pdf(pdf_filename=pdf_file, image_f_name=pdf_file.with_suffix('.png'))


def merge_pdfs_by_item_id(
    curr_contracts_id,
    subfolder_to_read_from: str = '_resulting_pdfs',
):

    from itertools import groupby
    from copy import deepcopy               # for progress bar only
    import tkinter as tk                    # for progress bar only
    from tkinter import ttk                 # for progress bar only

    def item_file_name(file: Path):
        """Skip file name middle part"""
        filename_parts = file.name.split("_")
        return "_".join(filename_parts[:3] + filename_parts[7:-2] + filename_parts[-1:])

    program_path = Path('.').resolve()  # .parent.parent.resolve()
    files_in_folder = (program_path / subfolder_to_read_from).iterdir()
    files_to_group = [
        file for file in files_in_folder
        if (file.suffix == ".pdf") and (int(file.name.split('_')[1]) == curr_contracts_id)
    ]

    total_files_num = len(files_to_group)   # for progress bar only
    root = tk.Tk()                          # for progress bar only
    progress = ttk.Progressbar(             # for progress bar only
        root, orient=tk.HORIZONTAL, length=total_files_num, mode='determinate'
    )
    progress.pack(pady=10)                  # for progress bar only

    files_merged = 0                        # for progress bar only
    for key, group in groupby(files_to_group, key=item_file_name):
        files_in_the_group = len(list(deepcopy(group)))  # for progress bar only
        utils.merge_pdfs(group, program_path / subfolder_to_read_from / key)
        files_merged += files_in_the_group  # for progress bar only
        progress['value'] = files_merged    # for progress bar only
        # Keep updating the master object to redraw the progress bar
        root.update()                       # for progress bar only

    root.mainloop()


def f_create_waybills_pdf(
    postman, state_pars: dict,
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

    showinfo(
        title='Створення pdf:',
        message="""
        Завершено!
        Підписуємо ЕН...
        """
    )

    subscribe_pdfs_stickers(curr_contracts_id)

    merge_pdfs_by_item_id(curr_contracts_id)

    showinfo(
        title='Створення файлів для друку:',
        message="Завершено!"
    )


if __name__ == "__main__":
    merge_pdfs_by_item_id(curr_contracts_id=6)
