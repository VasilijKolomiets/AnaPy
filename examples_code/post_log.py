# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import pandas as pd
import mysql.connector


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
    connection = mysql.connector.connect(user="root",  # 'username',
                                         host='localhost',
                                         database="artlogis_new",  # 'database_name'
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


def read_input_csvs(prods: Path, post_sets: Path) -> (pd.DataFrame, pd.DataFrame):
    _params = {
        'prods': {"df": None,
                  "col_names": ('id', 'title', 'short_delivery_id',
                                'weight', 'price_per_unit',  'img', )},
        'post_sets': {"df": None,
                      "col_names": ('id', 'short_order_id', 'user_id',
                                    'packs', 'amount', 'delivery_marker', )},
    }
    _params['prods']['df'] = pd.read_csv(prods, sep=";", encoding='cp1251', header=None)
    _params['prods']['df'].columns = _params['prods']["col_names"]
    _params['post_sets']['df'] = pd.read_csv(post_sets, sep=";", encoding='cp1251', header=None)
    _params['post_sets']['df'].columns = _params['post_sets']["col_names"]

    return (_params['prods']['df'], _params['post_sets']['df'])


if __name__ == '__main__':
    #  runfile('post_log.py', args='"изделия ноябрь.csv" "ДС ноябрь 2021.csv" ')
    #

    prods, post_sets = get_inline_params()
    # read the csv files to pandas DataFrames
    df_prods, df_post_sets = read_input_csvs(prods, post_sets)

    conn = from_server_connect()
    print(conn)
    my_cursor = conn.cursor()  # cursor created

    # work with the cursor here like printing initial database data

    # closing the cursor

    select = 'SELECT * FROM orders_full_list LIMIT 20'
    some_rows = my_cursor.execute(select)

    print(my_cursor.fetchall())

    my_cursor.close()
    # Disconnecting from the server
    conn.close()
