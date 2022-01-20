# -*- coding: utf-8 -*-
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

import pymysql

# server connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    database="artlogis_new",  # database created before
    passwd="MySQL_password#5"
)

my_cursor = mydb.cursor()  # cursor created

# work with the cursor here like printing initial database data

# closing the cursor

select = 'SELECT * FROM orders_full_list LIMIT 20'
some_rows = my_cursor.execute(select)

print(my_cursor.fetchmany(10))

my_cursor.close()
