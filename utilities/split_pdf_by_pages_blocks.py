# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 10:08:10 2021

inspiring source:
https://pythonist.ru/sozdanie-i-izmenenie-pdf-fajlov-v-python/

"""
from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path
# =============================================================================
#     Path.home()
#     / "creating-and-modifying-pdfs"
#     / "practice_files"
#     / "Pride_and_Prejudice.pdf"
# =============================================================================
here_path = Path(Path().absolute()).parent
pdf_path = here_path / '_work_pdf' / 'my_file_p2.pdf'

input_pdf = PdfFileReader(str(pdf_path.absolute()))

pages_quants_to_split = [8, 10, 1]
page_start, page_end_1 = 0, 0
for block_num, pages_quantity in enumerate(pages_quants_to_split):
    pdf_writer = PdfFileWriter()

    page_end_1 += pages_quantity
    for k in range(page_start, page_end_1):
        page = input_pdf.getPage(k)
        pdf_writer.addPage(page)
    page_start = page_end_1

    with (here_path / '_resulting_pdfs' / '_'.join(['del_me', str(block_num), '.pdf'])).open(
            mode="wb") as output_file:
        pdf_writer.write(output_file)
