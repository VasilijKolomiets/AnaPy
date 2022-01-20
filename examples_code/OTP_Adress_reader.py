# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 14:10:55 2021

@author: manager

Адреса	Начальник відділення	Телефон моб.


"""
import pandas as pd
from pprint import pprint
from pathlib import Path

import ua_posts_api

in_xlsxl_path = Path() / r"\IN_DATA\OTP_adressing.xlss"
df_sheet = pd.read_excel(in_xlsxl_path,
                         sheet_name='ритейл',
                         header=1,
                         usecols='E:G'
                         ).dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
print('readed')

df_sheet.columns = ('adress', 'boss', 'phone')  # set proper columns name
# rollout address by parts
df_sheet[['adr_zip', 'adr_city', 'adr_street', 'adr_building']
         ] = df_sheet['adress'].str.split(',', n=3, expand=True)
# remove starting 'вул.', 'м.' from  'adr_city', 'adr_street' columns respectively
df_sheet.adr_city = df_sheet.adr_city.str.split(n=1, expand=False).str[1].str.strip()
df_sheet.adr_street = df_sheet.adr_street.str.split(n=1, expand=False).str[1].str.strip()

#  convert apostrof "'"  into "`":
df_sheet.adr_city = df_sheet.adr_city.str.replace("'", "`")
df_sheet.adr_street = df_sheet.adr_street.str.replace("'", "`")

df_sheet.loc[:, 'city_ref'] = df_sheet['adr_zip']
df_sheet.loc[:, 'city_ref_json'] = df_sheet['adr_zip']

postman = ua_posts_api.Postman()
df_sheet.loc[:, 'city_ref'] = df_sheet.loc[:, 'city_ref'].apply(postman._city_by_ZIP_search_first)

df_1_result = df_sheet[df_sheet.city_ref.str.startswith('1_')].copy()
df_1_result.city_ref = df_1_result.city_ref.str[2:]     # save the CityRef - drop starting '1_'

df_many_results = df_sheet[~df_sheet.city_ref.str.startswith('1_')].copy()


for row in df_many_results.itertuples():  # try wise select true City from list of dict
    code, response_ = postman.search.by_zip_city_id(zipCode=row.adr_zip)
    city_ids = postman._city_by_ZIP_wise_pick(response_,
                                              city_name=row.adr_city,
                                              zipCode=row.adr_zip,
                                              )
    if not (type(city_ids) == type(list)):
        df_many_results.at[row.Index, 'city_ref'] = city_ids
    else:
        print("Ой біда: \n", city_ids)

df_sheet.to_excel("City_codes_by_ZIP.xlsx", engine='xlsxwriter')

res = postman.search.by_zip_city_id(zipCode='49055')

pprint(res)

# res2 = postman.parcels.create()
# `id`, `street_title`, `ref`, `build`, `street_ref`, `note`
