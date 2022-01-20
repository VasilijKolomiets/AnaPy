# -*- coding: utf-8 -*-

import sys
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
    connection = mysql.connector.connect(user = "root",  # 'username',
                                   host = 'localhost',
                                   database = "artlogis_new",  # 'database_name'
                                   passwd="MySQL_password#5"
                                   )
    return connection


if __name__ == '__main__':
    #  runfile('connect_mysql-connector-python.py', args='"изделия ноябрь.csv" "ДС ноябрь 2021.csv" ')
    #
    if len(sys.argv[1:]) != 2:
        sys.exit(""""потрібно 2 параметри - назви *.CSV файлів
                 Перший - вироби, другий - деталізація розсилки. Наприклад:

                 ")
    print(F"")
    conn = from_server_connect()
    print(conn)
    my_cursor = conn.cursor() #cursor created

    #work with the cursor here like printing initial database data

    #closing the cursor

    select = 'SELECT * FROM orders_full_list LIMIT 20'
    some_rows = my_cursor.execute(select)

    print(my_cursor.fetchall())



    my_cursor.close()
    # Disconnecting from the server
    conn.close()
