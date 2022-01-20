# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 09:37:41 2021

@author: manager

Заголовки стовпців csv  файлу
"Назва області";Назва району;Назва населеного пункту (повна);Поштовий індекс населеного пункту;Назва вулиці;Номер будинку;Назва відділення зв'язку;Поштовий індекс в_дд_лення зв'язку (ВПЗ);Region (Oblast);Distinct (Rayon);Locality;Postindex Locality;Street;House_numbers;Post office;Postindex VPZ

"""
import pandas as pd
from pathlib import Path

path_ro_csv = Path(r'..\IN_DATA\zipCodes.csv')


def init():
    global df_indx
    df_indx = pd.read_csv(path_ro_csv,
                          encoding='cp1251', sep=';',
                          # skiprows=2
                          )
    return df_indx


def zips_by_city_nd_street(df_indx, city_name: str, street_name: str) -> tuple:

    if city_name in df_indx["Назва населеного пункту (повна)"].unique():
        rez = tuple(df_indx[
            df_indx["Назва населеного пункту (повна)"].str.contains(city_name)
            & df_indx["Назва вулиці"].str.contains(street_name)
        ]["Поштовий індекс населеного пункту"], )

        return str(rez[0]) if len(rez) == 1 else rez
    else:
        return tuple()


if __name__ == '__name__':
    city_name, street_name = 'Біла Церква', 'вул. Олександрійська, 101'
    city_name, street_name = 'Волочиськ',	'вул. Незалежності, 104'
    city_name, street_name = 'Рівне',	'вул. Директорії, 6'

    print(zips_by_city_nd_street(city_name,
                                 street_name.split(',')[0].split()[-1])
          )
