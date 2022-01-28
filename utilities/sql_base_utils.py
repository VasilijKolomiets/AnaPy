# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 11:31:20 2022

@author: manager
"""
import requests

from model import (
    add_row_values_to_DB,
    update_meest_streets,
)


def f_cities_refresh(state_pars: dict):
    if state_pars['post_service']['id_postcervices'] == 1:  # MeestExpress
        print("Почекайте.")
        response = requests.post('https://publicapi.meest.com/geo_localities')
        """
        {'data': {'n_ua': 'Білошапки',
          'n_ru': 'Белошапки',
          't_ua': 'село',
          'city_id': '44ac840c-749b-11df-b112-00215aee3ebe',
          'kt': '7424180601',
          'reg': 'ЧЕРНІГІВСЬКА',
          'dis': 'Прилуцький',
          'd_id': '78f453ca-41b9-11df-907f-00215aee3ebe'}},
        """

        result_list = response.ok and [data['data'] for data in response.json()['result']] or []
        print("Почекайте... хвилин 5.")
        for city_data in result_list:
            add_row_values_to_DB('directory_meest_cities', city_data)
        print("Завершуємо...")

        update_meest_streets()  # TODO: have to rewrite this procedure !!!
        print("Готово!")


def f_streets_refresh(state_pars: dict):
    if state_pars['post_service']['id_postcervices'] == 1:  # MeestExpress
        print("Почекайте.")
        response = requests.post('https://publicapi.meest.com/geo_localities')
        """
        {'data': {'n_ua': 'Білошапки',
          'n_ru': 'Белошапки',
          't_ua': 'село',
          'city_id': '44ac840c-749b-11df-b112-00215aee3ebe',
          'kt': '7424180601',
          'reg': 'ЧЕРНІГІВСЬКА',
          'dis': 'Прилуцький',
          'd_id': '78f453ca-41b9-11df-907f-00215aee3ebe'}},
        """

        result_list = response.ok and [data['data'] for data in response.json()['result']] or []
        print("Почекайте... хвилин 5.")
        for city_data in result_list:
            add_row_values_to_DB('directory_meest_cities', city_data)
        print("Завершуємо...")

        update_meest_streets()  # TODO: have to rewrite this procedure !!!
        print("Готово!")
