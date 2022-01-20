# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 15:14:28 2021

@author: Vasil
"""
from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path

# Path.home()  ::=  'C:\\Users\\Vasil\\'
pdf_path = Path() / '_work_pdf' / 'my_file_p__2.pdf'

input_pdf = PdfFileReader(str(pdf_path))


for page in range(input_pdf.getNumPages()):
    pdf_writer = PdfFileWriter()
    current_page = input_pdf.getPage(page)
    pdf_writer.addPage(current_page)

    outputFilename = "example-page-{}.pdf".format(page + 1)
    with open(outputFilename, "wb") as out:
        pdf_writer.write(out)

        print("created", outputFilename)
