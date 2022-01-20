# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 16:27:32 2021

@author: manager
"""
from settings import credentials
import ua_posts_api

postman_del = ua_posts_api.Postman(credentials['Meest'])

date = '19.01.2022'
code, resp = postman_del.parcels.get_all_on_date(date)

parcels_cout, deleted_parcels_count = len(resp), 0
for di in resp:
    di_code, di_resp = postman_del.parcels.delete_by_id(parcel_id=di["parcelID"])
    if di_code == 200:  # and di_resp["status"] == 'Ok'
        deleted_parcels_count += 1

print(deleted_parcels_count)
