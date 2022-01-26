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


tables_fields = {
    'companies': ['id', 'is_active', 'company_name', 'short_name_latin', 'code_EDRPOU', 'phone']
}

widgets_table = {
    'companies': {
        "minsize": (600, 240),
        "title": "companies",

        # list of forms entries with their names:
        "entries": {
            # 'id': {'text': 'entry_1_name'},
            # 'is_active': {'text': 'entry_2_name'},
            'company_name': {'text': 'Назва Компанії', 'type': str},
            'short_name_latin': {'text': 'Коротка назва латиницею', 'type': str},
            'code_EDRPOU': {'text': 'Код ЄДРПОУ', 'type': int},
            'phone': {'text': 'Контактний телефон', 'type': str}
        },
    }
}

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
TODO: list of TODOS )

2022-01-21

Done-2022-01-26: не визначено місто - CityID. 1) list або 2) empty.  - програма падає.
Done-2022-01-26: жодної вулиці не знайдено. Токена немає - програма падає.
Done-2022-01-24: невірно рахується вага
Done-2022-01-24: невірно нарізаються PDF
Done-2022-01-24: Об'єднати нарізані PDF у файл групуючи відповідно продукції.
                 Одна продукція - один файл
Done-2022-01-26: перевірити - сортування відповідно ваги по файлах ? натяк на пошук помилки
Done-2022-01-21: змінити аостроф у прізвищах та іменах наповоротний
Done-2022-01-21: під час зчитування даних - .strip() - імена, назви, всюди, де є літери!!
Done-2022-01-24: підписати непорізані експрес накладні в PDF.
TODO: створити реєстр замовлення міст.
Done-2022-01-24: повідомлення після створення PDF файлів, або прогресс - бар.

2022-01-24
TODO: перевіряти адреси під час додання нової адреси на предмет існування за параметрами:
    місто (код) / вулиця (код) / будинок / ПІБ (???) / Телефон (???)
TODO: ??? при записуванні нового товару (тіки-но зчитаного з файлу)
    перевіряти на наявність точно такого в базі і не додавати,  а повертати ID існуючого товару
TODO:


2022-01-26
TODO: Створення точки отримання вручну, інтерактивно вибираючи параметри адреси
TODO: Вивантажити (в ексель): існуючі адреси / поточний розподіл відправлень / (ще щось?)
TODO: Створення "вручну" поставки / клієнта / (ще щось?)
TODO: Під час вибору файла в меню вибору файла під час натискання на <ESC> - програма "падає"
TODO: Після групового внесення даних з файлу повідомляти результат типу:
      - Х1 рядків прочитано з файлу
      - Х2 позицій вже було в базі (не нові)
      - Х3 не вдалося опрацювати повністтю (пропущено)
      результат опрацювання записано в файл з назвою:  "назва файлу"

TODO: якщо програма під час внесення розподілу подукції по одержувачам програма падає - що
    робити з тими рядками, що вже прочитано / внесено в базу як нові?

TODO: під час опрацювання довготермінових процесів повсюди виводити прогресбар
TODO: під час вибору вулиці (вже після вибору) натискання на відміну має наново запускати вибір
     ??? перевірити, що буде при натисканні на <ESC>

2022-01-27
TODO: Нова Пошта!



TODO:
"""
