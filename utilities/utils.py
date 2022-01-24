# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 09:37:41 2021

@author: manager

Заголовки стовпців csv  файлу
"Назва області";Назва району;Назва населеного пункту (повна);Поштовий індекс населеного пункту;Назва вулиці;Номер будинку;Назва відділення зв'язку;Поштовий індекс в_дд_лення зв'язку (ВПЗ);Region (Oblast);Distinct (Rayon);Locality;Postindex Locality;Street;House_numbers;Post office;Postindex VPZ

"""
import pandas as pd
from pathlib import Path

import fitz   # <-- PyMuPDF
from PIL import Image, ImageDraw, ImageFont

path_ro_csv = Path(r'..\IN_DATA\zipCodes.csv')


def ФИО_to_surname_name_middlename(ФИО: str):
    full_name = ФИО.split()
    surname = full_name[0]
    middlename, name = "Х", "Х"
    if len(full_name) == 3:
        middlename = full_name[2]
    if len(full_name) >= 2:
        name = full_name[1]
    return (surname, name, middlename)


def init():
    global df_indx
    df_indx = pd.read_csv(path_ro_csv,
                          encoding='cp1251', sep=';',
                          # skiprows=2
                          )
    return df_indx


def zips_by_city_nd_street(df_indx, city_name: str, street_name: str) -> tuple:

    if any(df_indx["Назва населеного пункту (повна)"].str.contains(city_name)):
        rez = tuple(df_indx[(df_indx[
            "Назва населеного пункту (повна)"].str.contains(city_name))
            & (df_indx["Назва вулиці"].str.contains(street_name))
        ]["Поштовий індекс населеного пункту"], )

        return str(rez[0]) if len(rez) == 1 else rez
    else:
        return tuple()


def txt_to_image_EN(text_str: str, out_file: str = 'text.png', img_size=(226*3, 32*3),
                    font_ttf: str = 'arial.ttf', font_size: int = 42):

    img = Image.new('RGB', img_size, (255, 255, 255))

    font = ImageFont.truetype(font_ttf, size=42, encoding='UTF-8')  # 'monocondensedc1.ttf'
    draw = ImageDraw.Draw(img)

    # draw.text((10, 10), str) -- ошибка
    # draw.text((10, 1), text_str, font=font, fill=(0, 0, 0))

    # draw multiline text
    draw.multiline_text((1, 1), text_str, font=font, fill=(0, 0, 0))

    # img.show()
    img.save(out_file)


def image_to_pdf(pdf_filename: str = 'some.pdf', rect_coord=(0, 114, 212, 136), image_f_name=None):

    rect = fitz.Rect(rect_coord)         # where to put image: use upper left corner

    doc = fitz.open(str(pdf_filename))   # open the PDF
    for page in doc:
        #  print(page.rect)  ->  Rect(0.0, 0.0, 283.44000244140625, 283.44000244140625)
        page.insert_image(rect, filename=str(image_f_name))

    doc.saveIncr()                       # do an incremental save


def merge_pdfs(files_from, file_to):
    # import fitz
    result = fitz.open()

    for pdf in files_from:
        with fitz.open(pdf) as mfile:
            result.insert_pdf(mfile)

    result.save(file_to)


if __name__ == '__main__':
    city_name, street_name = 'Біла Церква', 'вул. Олександрійська, 101'
    city_name, street_name = 'Волочиськ',	'вул. Незалежності, 104'
    city_name, street_name = 'Рівне',	'вул. Директорії, 6'

    print(zips_by_city_nd_street(city_name, street_name.split(',')[0].split()[-1]))
