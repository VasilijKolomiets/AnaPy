"""[summary]
"""
import mysql.connector as connector  # mysql.connector.python
import sys
from pathlib import Path

global temp_cursor


def from_server_connect():
    """
    Spyder Editor
    artlogis_new&password=t6zdxzfn
    artlogis_mysql_ukraine_com_ua.sql
    This is a temporary script file.

    +------------------------+
    | Tables_in_artlogis_new |
    +------------------------+
    | addresses              |
    | cities                 |
    | city_to_company        |
    | companies              |
    | deliveries_full_list   |
    | deliveries_short_list  |
    | orders_full_list       |
    | orders_short_list      |
    | users                  |
    | users_old              |
    +------------------------+

    """
    # Connecting from the server
    connection = connector.connect(user="root",               # 'username',
                                   host='localhost',
                                   database="postman",         # 'database_name'
                                   passwd="MySQL_password#5"
                                   )
    return connection


def get_inline_params(data_folder: str = r'.\IN_DATA') -> (Path, Path):
    if len(sys.argv[1:]) != 2:
        sys.exit(
            """
            Потрібно 2 параметри - назви *.CSV файлів.
            Перший - вироби, другий - деталізація розсилки. Наприклад:

            > python post_log.py изделия_ноябрь.csv ДС_ноябрь_2021.csv
            """
        )
    print(F"Отримано {len(sys.argv[1:])} параметрів, а саме: \n {sys.argv[1:]}")

    return (Path(data_folder) / file_name for file_name in sys.argv[1:])


credentials = {
    'Meest': {
        'url':      r'https://api.meest.com/v3.0/openAPI',
        'username': r'art-pres_vkf_dnipro',
        'password': r'A^fFsnJR0OLG',
        'contract_id': "a3df71d8-5e17-11ea-80c6-000c29800ae7",
        'content_type': 'application/json',
    },
    'NovaPoshta': {
        'url':      r'https://api.meest.com/v3.0/openAPI',
        'username': r'art-pres_vkf_dnipro',
        'password': r'A^fFsnJR0OLG',
        'contract_id': "a3df71d8-5e17-11ea-80c6-000c29800ae7",
        'content_type': 'application/json',
    }
}


state_params = dict(
    client=dict(id_companies=None, name=None),
    delivery_contract=dict(id_delivery_contract=None, name=None),
    post_service=dict(id_postcervices=None, name=None),
    statusbar=None,
    selected_street=dict(id_street=None, name=None),
)

"""========= Meest =========

https://wiki.meest-group.com/api/ua/v3.0/openAPI#/


"""
{
    "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
    "receiverPay": False,
    # "COD": 600,
    "notation": "коментар який буде надрукований на накладній",
    "sender":
        {"phone": "+38050-421-1558",
         "name": 'Васина Лариса',
         "service": "Door",
         "addressID": "d3d482e3-ed9f-11df-b61a-00215aee3ebe",
         "building": "10A",
         "floor": 1,
         "notation": ".....",
         },
    "placesItems": [
            {"weight": 0.101,
             "height": 5,
             "width":  4,
             "length": 7,
             "insurance": 10.0,
             "quantity": 5,
             }
            ],
    "receiver": {
        "name": "Ромась Оксана",
        "phone": "+38050-449-3840",
        "zipCode": "21029",
        "addressID": "743fdc85-e0d2-11df-9b37-00215aee3ebe",
        "building": "35А",
        "flat": "1",
        "floor": 1,
        "service": "Door",
            },

    "payType": "noncash",
}


{
    "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
    "payType": "noncash",
    "receiverPay": "false",
    "expectedPickUpDate": {
        "date": "20.01.2022",
        "timeFrom": "15:00",
        "timeTo": "18:00"
    },
    "sender": {
        "name": "Васина Лариса ",
        "phone": "+38050-421-1558",
        "addressID": "d3d482e3-ed9f-11df-b61a-00215aee3ebe",
        "building": "10А",
        "service": "Door",
        "notation": "Типографія Арт-Прес, м. Дніпро"
    },
    "parcelsItems": [
        {
            "parcelId": "a453dbbd-7a0b-11ec-80e4-000c29800ae7"
        },
        {
            "parcelId": "a453dbc6-7a0b-11ec-80e4-000c29800ae7"
        },
        {
            "parcelId": "a453dbca-7a0b-11ec-80e4-000c29800ae7"
        },
        # ...
    ]
}

"""
2022-01-21

TODO: не визначено місто - CityID. 1) list або 2) empty.  - програма падає.
TODO: жодної вулиці не знайдено. Токена немає - програма падає.
Done-2022-01-24: невірно рахується вага
Done-2022-01-24: невірно нарізаються PDF
Done-2022-01-24: об'єднати нарізані PDF у файл групуючи відповідно продукції. Одна продукція - один файл
TODO: перевірити - сортування відповідно ваги по файлах ? натяк на пошук помилки
Done-2022-01-21: змінити аостроф у прізвищах та іменах наповоротний
Done-2022-01-21: під час зчитування даних - .strip() - імена, назви, всюди, де є літери!!
Done-2022-01-24: підписати непорізані експрес накладні в PDF.
TODO: створити реєстр замовлення міст.
Done-2022-01-24: повідомлення після створення PDF файлів, або прогресс - бар.



"""
