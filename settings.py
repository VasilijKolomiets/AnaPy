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



authentication ------------------------------------------------------------
Аутентифікація

POST
/auth
Аутентифікація користувача

curl --location --request POST 'https://api.meest.com/v3.0/openAPI/auth' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "username",
    "password": "password"
}'

Response example::
{
  "status": "OK",
  "info": {
    "fieldName": "",
    "message": "",
    "messageDetails": ""
  },
  "result": {
    "token": "8664e2d0ec36e124034a69ef92be5838",
    "expiresIn": "86400",
    "refreshToken": "71e9bcf55d44c46a0d63b0cf3e5dc6ba"
  }
}


POST
/refreshToken
Оновлення токена

curl --location --request POST 'https://api.meest.com/v3.0/openAPI/refreshToken' \
--header 'Content-Type: application/json' \
--header 'token: 5c3749e3598ef423b092b7daf8405206' \
--data-raw '{
    "refreshToken": "a20290cd049fbb81eba8912fc12f4845"
}'

Response example::
{
  "status": "OK",
  "info": {
    "fieldName": "",
    "message": "",
    "messageDetails": ""
  },
  "result": {
    "token": "01b75dc45d28a3ad9e203152680cf646",
    "expiresIn": "1000000",
    "refreshToken": "951f25a11f243a43771f139124900102"
  }
}


search ------------------------------------------------------------
Функції пошуку адміністративно-територіальних одиниць та підрозділів

POST
/getAddressByCoord
Отримання адресу за координатами

POST
/addressSearchByCoord
Пошук адреси за координатами

POST
/countrySearch
Пошук країни

POST
/regionSearch
Пошук області

POST
/citySearch
Пошук населеного пункту

GET
/zipCodeSearch/{zipCode}
Пошук населеного пункту за поштовим індексом

POST
/addressSearch
Пошук адреси

GET
/branchTypes
Довідник типів відділень

POST
/branchSearch
Пошук підрозділу

GET
/branchSearchGeo/{latitude}/{longitude}/{radius}
Пошук найближчого підрозділу за географічними координатами

GET
/branchSearchLocation/{latitude}/{longitude}/{radius}
Пошук найближчого підрозділу

curl --location --request GET 'https://api.meest.com/v3.0/openAPI/branchSearchLocation/49.9671230/36.2205240/200' \
--header 'Content-Type: application/json' \
--header 'token: 5c3749e3598ef423b092b7daf8405206'


Response example::
{
  "status": "OK",
  "info": {
    "fieldName": "",
    "message": "",
    "messageDetails": ""
  },
  "result": [
    {
      "branchID": "8893174e-79c8-11ea-80c6-000c29800ae7",
      "branchIDref": "0x80C6000C29800AE711EA79C88893174E",
      "branchNo": 9550,
      "branchType": "АПТ",
      "branchTypeID": "23c4f6c1-b1bb-49f7-ad96-9b014206fe8e",
      "branchTypeDescr": "Поштомат: до 30 кг.",
      "branchTypeAPP": "3",
      "networkDepartment": true,
      "networkPartner": "Супермаркет АТБ",
      "networkPartnerCode": "005",
      "branchDescr": {
        "descrUA": "Поштомат №9550",
        "descrSearchUA": "Харків вул. Москалівська (Жовтневої Революції),106"
      },
      "addressID": "f0c347c5-eda2-11df-b61a-00215aee3ebe",
      "addressDescr": {
        "descrUA": "вул. Москалівська (Жовтневої Революції) ",
        "descrRU": "ул. Москалевская (Октябрской Революции)",
        "descrEN": "Moskalivska (Zhovtnevoi Revoliutsii) st."
      },
      "addressMoreInformation": "Супермаркет АТБ",
      "cityID": "87162365-749b-11df-b112-00215aee3ebe",
      "cityDescr": {
        "descrUA": "Харків",
        "descrRU": "Харьков",
        "descrEN": "Kharkiv"
      },
      "districtID": "fbfb8c27-41be-11df-907f-00215aee3ebe",
      "districtDescr": {
        "descrUA": "Харків",
        "descrRU": "Харьков",
        "descrEN": "Kharkiv"
      },
      "regionID": "d15e302c-60b0-11de-be1e-0030485903e8",
      "regionDescr": {
        "descrUA": "ХАРКІВСЬКА",
        "descrRU": "ХАРЬКОВСКАЯ",
        "descrEN": "HARKIVS`KA"
      },
      "workingHours": "Пн-Нд 00:00-23:59",
      "building": "106",
      "zipCode": "61004",
      "latitude": 49.967123,
      "longitude": 36.220524,
      "branchWorkTime": [
        {
          "day": "Пн",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Вт",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Ср",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Чт",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Пт",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Сб",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        },
        {
          "day": "Нд",
          "timeFrom": "00:00",
          "timeTo": "23:59",
          "LunchBreakFrom": "",
          "LunchBreakTo": ""
        }
      ],
      "phone": "",
      "address": "Харків вул. Москалівська (Жовтневої Революції),106",
      "paymentTypes": "",
      "branchLimits": {
        "weightTotalMax": 29.99,
        "volumeTotalMax": 0.08,
        "insuranceTotalMax": 15000,
        "weightPlaceMax": 0,
        "quantityPlacesMax": 0,
        "gabaritesMax": {
          "length": 61,
          "width": 37,
          "height": 35
        },
        "formatLimit": true,
        "cashPayUnavailible": true,
        "sendingOnly": false,
        "receivingOnly": false,
        "receiverCellPhoneRequired": true,
        "terminalCash": false
      }
    }
  ]
}

GET
/payTerminalSearch/{latitude}/{longitude}/{radius}
Пошук найближчих місць оплат



parcels ------------------------------------------------------------
Функції для роботи з відправленнями

GET
/parcelStatus/{parcelID}
Статуси відправлення

GET
/EasyReturnAgentInfo
Інформація про агента

GET
/parcelStatusDetails/{parcelID}
Статуси відправлення (детально)

GET
/getParcel/{parcelID}/{searchMode}/{returnMode}
Перегляд параметрів відправлення

POST
/parcelChangeReceiver
Зміна отримувача

GET
/timeSlot
часові діапазони доставки | забору

PUT
/parcelChangeContractID
Зміна агента

GET
/parcelDebtInfo/{parcelID}/{IDAgent}/{ByMerchants}
Отримати борг по посилці

POST
/parcel
Створення відправлення
повний опис усих існуючих поль запиту:
https://documenter.getpostman.com/view/12823986/TVRq1QqQ#622b9f56-b4bb-421c-b4cd-59058710c306

curl --location --request POST 'https://api.meest.com/v3.0/openAPI/parcel' \
--header 'Content-Type: application/json' \
--header 'token: 5c3749e3598ef423b092b7daf8405206' \
--data-raw '{
    "parcelNumber": "7770000001",
    "notation": "Test API parcel",
    "contractID": "4a430ffd-6b7d-11e2-a79e-003048d2b473",
    "payType": "cash",
    "receiverPay": false,
    "COD": 2000,
    "sender": {
        "name": "Surname Name Patronymic",
        "phone": "+1-234-567-8901",
        "zip": "07064",
        "branchID": "67ff661b-77b8-11e0-88cf-00215aee3ebe",
        "service": "Branch"
    },
    "receiver": {
        "name": "Surname Name Patronymic",
        "phone": "+1-234-567-8901",
        "zip": "",
        "branchID": "0d161467-ffac-11e8-80d9-1c98ec135261",
        "service": "Branch"
    },
    "contentsItems": [
        {
            "contentName": "socks",
            "quantity": 10,
            "weight": 10,
            "value": 30
        },
        {
            "contentName": "boots",
            "quantity": 10,
            "weight": 10,
            "value": 30
        }
    ]
}'


Response example::
{
  "status": "OK",
  "info": {
    "fieldName": "",
    "message": "",
    "messageDetails": ""
  },
  "result": {
    "parcelID": "a60ac654-0d3a-11eb-80cd-000c29800ae7",
    "barCode": "CR049358941US"
  }
}

POST
/parcelGeo
Створення відправлення

PUT
/parcelGeo/{parcelID}
Редагування відправлення

PUT
/parcel/{parcelID}
Редагування відправлення

DELETE
/parcel/{parcelID}
Вилучення відправлення

curl --location --request DELETE 'https://api.meest.com/v3.0/openAPI/parcel/7f2a12c6-0894-11eb-80cd-000c29800ae7' \
--header 'Content-Type: application/json' \
--header 'token: 5c3749e3598ef423b092b7daf8405206'

Response example::
{
  "status": "OK",
  "info": {
    "fieldName": "",
    "message": "",
    "messageDetails": ""
  },
  "result": {}
}


GET
/parcelsList/{dateFrom}
Перелік створених відправлень певною датою

GET
/orderDateInfo/{streetID}
список дат виклику кур'єра

POST
/calculate
Розрахунок вартості послуг та дати доставки

GET
/packTypes
Довідник видів пакувань

GET
/specConditions
Довідник додаткових послуг

GET
/info4Sticker/{parcelID}
Інформація для самостійного друку Стікера

GET
/photoFixation/{number}
функція для отримання вкладених файлов під час доручення

GET
/parcelGoodsReturn/{parcelID}
список товару на повернення по відправленню

POST
/LockParcel
Блокує доставку посилки

POST
/UnlockParcel
Розблоковує доставку заблокованої посилки



registers ------------------------------------------------------------
Формування реєстрів відправлень, виклик кур`єра

POST
/registerBranch
Створення реєстру відправлень - СКЛАД

PUT
/registerBranch/{registerID}
Редагування реєстру відправлень - СКЛАД

DELETE
/registerBranch/{registerID}
Вилучення реєстру відправлень - СКЛАД

POST
/registerPickup
Формування реєстру відправлень та заявки на виклик - КУР'ЄРА

PUT
/registerPickup/{registerID}
Редагування реєстру відправлень та заявки на виклик - КУР'ЄРА

DELETE
/registerPickup/{registerID}
Скасування виклику кур'єра

GET
/registersList/{dateFrom}
Перелік створених реєстрів певною датою



print ------------------------------------------------------------
Друковані форми

GET
/print/declaration/{printValue}/{contentType}
Декларація

GET
/print/register/{printValue}/{contentType}
Реєстр

GET
/print/cn23/{printValue}/{contentType}
Митна декларація Cn23

GET
/print/sticker/{printValue}/{contentType}/{termoprint}
Стікер

GET
/print/sticker100/{printValue}
GET

/print/sticker100A4
Друк стікера 100х100 на А4



tracking ------------------------------------------------------------
Трекінг

GET
/tracking/{trackNumber}
Відстеження поштового відправлення

GET
/trackingDelivered/{dateFrom}/{dateTo}/{page}
Доручені відправлення за період

GET
/trackingByDate/{searchDate}
Події з посилками за обраний день

GET
/parcelInfoTracking/{parcelID}

GET
/trackingByPeriod/{dateFrom}/{dateTo}
Трекінг по періоду до двох годин



other ------------------------------------------------------------
додаткові функції

GET
/banners

full descriptions of POST /parsel parameters:

{	object	required                                                     ------------
Main {object} block start
parcelNumber	string	optional	TST-2550636	Shipment number            ------------
subAgent	string	optional	546234532	ID of delivery payeer
notation	string	optional	notation	Notation, comment                 -------------
contractID	string	optional	4a430ffd-6b7d-11e2-a79e-003048d2b473	Unique customer ID. Assigned after creating a client in the system
payType	string	required	cash	Payment type. Options: cash, noncash    ------------
receiverPay	boolean	required	true	Who pays for the shipment. «false» - Sender, «true» - Receiver        ------------
COD	number($float)	optional	1200	Postpay / return shipping value. Type: float(8,2)
sendingDate	string	optional	19.03.2019	Shipment date. If this parameter is empty, the “estimatedDeliveryDate” parameter will not be calculated in the response. Format: dd.MM.yyyy
info4Sticker	boolean	optional	true
expectedDeliveryDate	object	optional
Expected Delivery Date {object} block
{	object	optional
Expected Delivery Date {object} block start
date	string	optional	16.09.2020	Desired delivery date. Skipped if service == Branch. To pre-evaluate the availability of a date, use the calculate function - it will confirm the desired delivery date or offer 14 alternative dates. Format: dd.MM.yyyy
timeFrom	string	optional	10:00	Start of desired delivery range. Skipped if service == Branch. Format: hh:mm
timeTo	string	optional	12:00	End of desired delivery range. Skipped if service == Branch. Format: hh:mm
}	object	optional
Expected Delivery Date {object} block end
sender	object	required                                                  ------------
Sender {object} block
{	object	required                                                        ------------
Sender {object} block start
name	string	required	Dawn Lyons	Sender name                           ------------
phone	string	required	+1-202-555-0171	Sender phone                       ------------    ------------
zip	string	optional	12601	Sender postal code
branchID	string	required	328a79e5-8452-11e8-80d4-1c98ec135261	Unique sender Branch ID identifier. Obtained by “branchSearch” function. Required if service == Branch
addressID	string	required	da9108ea-e0d3-11df-9b37-00215aee3ebe	Unique sender Address ID. Obtained by “addressSearch” function. Required if service == Door
building	string	required	3	Sender building number. Required if service == Door
flat	string	optional	454	Sender flat number
floor	integer($int32)	optional	4	Sender floor number
service	string	required	Door	Delivery type options: Door, Branch
}	object	required                                                           ------------
Sender {object} block end
receiver	object	required                                                   ------------
Receiver {object} block
{	object	required                                                          ------------
Receiver {object} block start
name	string	required	Peter Peterson	Receiver name                        ------------
phone	string	required	+380920639860	Receiver phone                         ------------
zip	string	required	98891	Receiver postal code                            ------------   ------------
branchID	string	required	f652c0c9-8b60-11e8-80d4-1c98ec135261	Unique receiver Branch ID identifier. Obtained by “branchSearch” function. Required if service == Branch
addressID	string	required	6e23d513-e0d2-11df-9b37-00215aee3ebe	Unique receiver Address ID. Obtained by “addressSearch” function. Required if service == Door
building	string	required	50	Receiver building number. Required if service == Door
flat	string	optional	122	Receiver flat number
floor	integer($int32)	optional	8	Receiver floor number
service	string	required	Branch	Delivery type. Options: Door, Branch         ------------
}	object	required                                                             ------------
Receiver {object} block end
placesItems	array	required                                                     ------------
Places Items [array] with {object}s block
[	array	required                                                                ------------
Places Items [array] block start
{	object	required                                                             ------------
Places Items {object} block start
quantity	integer($int32)	required	1	Places quantity                          ------------
weight	number($float)	required	0.589	Weight, kg. Type: float(8,3)           ------------
volume	number($float)	optional	5.121	Volume. Type: float(7,3)               ------------
insurance	number($float)	optional	200	Declared value of shipping. Type: float(9,2)
packID	string	optional	c26956ba-a2ce-11e4-b90b-003048d2b473	Unique pack ID. Obtained by “packTypes” function
length	integer($int32)	optional	20	Length, cm                                 ------------
width	integer($int32)	optional	30	Width, cm                                   ------------
height	integer($int32)	optional	10	Height, cm                                ------------
wheels	string	optional	r13	Wheels radius
}	object	optional                                                                   - - - - -
Places Items {object} block end
]	array	optional
Places Items [array] block end
specConditionsItems	array	optional
Spec Conditions Items [array] with {object}s block
[	array	optional
Spec Conditions Items [array] block start
{	object	optional
Spec Conditions Items {object} block start
conditionID	string	optional	9c6c4d1e-b2cc-11e0-a658-003048d2b473	Unique delivery condition ID. Obtained by “specConditions” function
}	object	optional
Spec Conditions Items {object} block end
]	array	optional
Spec Conditions Items [array] block end
contentsItems	array	optional
Contents Items [array] with {object}s block
[	array	optional
Contents Items [array] block start
{	object	optional
Contents Items {object} block start
contentName	string	required	trouses	Content name
quantity	integer($int32)	required	1	Content quantity, units
weight	number($float)	required	22.785	Content weight, kg. Type: float(8,3)
value	number($float)	required	100.12	Content value. Type: float(9,2)
customsCode	string	optional	200	Сustoms сode
country	string	optional	DE	Country of origin
}	object	optional
Contents Items {object} block end
]	array	optional
Contents Items [array] block end
codPaymentsItems	array	optional
COD Payments Items [array] with {object}s block
[	array	optional
COD Payments Items [array] block start
{	object	optional
COD Payments Items {object} block start
agentId	string	required	546234532	EDRPOU of the recipient of funds                ----  -- -- ----
cod	number($float)	required	1200	The amount of funds from the total COD          --- -- -- -- ---
}	object	optional
COD Payments Items {object} block end
]	array	optional
COD Payments Items [array] block end
goods	array	optional
Goods [array] with {object}s block
[	array	optional
Goods [array] block start
{	object	optional
Goods {object} block start
article	string	required	651-24523	article                                         - -- --- ------
name	string	required	monitor	name                                                --- - ---- ----
serialNumber	string	optional	SN34943516546546	Serial Number
weight	number($float)	required	12	Weight                                        ---  ------- --
quantity	integer($int32)	required	2	Quantity                                      --- ----- -- --
price	number($float)	required	8700	Price                                         - -- ---- - ---
length	number($float)	optional	130	Lenght
width	number($float)	optional	25	Width
height	number($float)	optional	75	Height
}	object	optional
Goods {object} block end
]	array	optional
Goods [array] block end
}	object	required                                                                 ------------
Main {object} block end
====================================================
JSON
====================================================
{	                                          -----------
parcelNumber	string	                      -----------  optional	TST-2550636	Shipment number
notation	string                            -----------  optional	notation	Notation, comment
payType	string	                            -----------  required	cash	Payment type. Options: cash, noncash
receiverPay	false	        	                -----------  required	false Who pays for the shipment. «» - Sender, «true» - Receiver
sendingDate	19.03.2019	                     - - - - - - optional	19.03.2019	Shipment date. If this parameter is empty, the “estimatedDeliveryDate” parameter will not be calculated in the response. Format: dd.MM.yyyy
  sender: {	                                            -----------  object	required
            name	string	                              -----------  required	Dawn Lyons	Sender name
            phone	string	                              -----------  required	+1-202-555-0171	Sender phone
            zip	string	                                - - - - - -  optional	12601	Sender postal code
            branchID	                                  -----------  string	required	328a79e5-8452-11e8-80d4-1c98ec135261	Unique sender Branch ID identifier. Obtained by “branchSearch” function. Required if service == Branch
            service	string	required	Branch            -----------  Delivery type options: Door, Branch
          }	                                            -----------  object	required


receiver: {                                            -----------  object	required    receiver	object	required
            name:	string	                              -----------  required	Peter Peterson	Receiver name
            phone:	string	                              -----------  required	+380920639860	Receiver phone
            zip:	string	                                -----------  required	98891	Receiver postal code
            addressID	string	required	6e23d513-e0d2-11df-9b37-00215aee3ebe	Unique receiver Address ID. Obtained by “addressSearch” function. Required if service == Door
            building:	string	required	50	Receiver building number. Required if service == Door
            flat:	string	optional	122	Receiver flat number
            floor:	integer($int32)	optional	8	Receiver floor number
            service:	'Door'	                            ------------  required	Branch	Delivery type. Options: Door, Branch
          }                                           ------------  object	required

[                                           ------------  placesItems	array	required  Places Items [array] with {object}s block
{	                                          ------------  Places Items {object} block start
contentName: "Поліграфія"	                  ------------  string	required	trouses	Content name            %%%%
serialNumber	                              - -- -- -- -   string	optional	SN34943516546546	Serial Number %%%%
quantity	1	                                ------------  required	1	Places quantity
weight	number($float)                      ------------ 	required	0.589	Weight, kg. Type: float(8,3)
volume	number($float)	                    - -- -- -- -  optional	5.121	Volume. Type: float(7,3)
insurance	number                            - -- -- -- -  ($float)	optional	200	Declared value of shipping. Type: float(9,2)
packID	string	                            - -- -- -- -  optional	c26956ba-a2ce-11e4-b90b-003048d2b473	Unique pack ID. Obtained by “packTypes” function
length	integer($int32)	                    - -- -- -- -  optional	20	Length, cm
width	integer($int32)	                      - -- -- -- -  optional	30	Width, cm
height	integer($int32)	                    - -- -- -- -  optional	10	Height, cm
}	                                                            - -- -- -- -

]	array	optional

contentsItems	array	optional
Contents Items [array] with {object}s block
[	array	optional
Contents Items [array] block start
{	object	optional
Contents Items {object} block start
contentName	string	required	trouses	Content name
quantity	integer($int32)	required	1	Content quantity, units
weight	number($float)	required	22.785	Content weight, kg. Type: float(8,3)
value	number($float)	required	100.12	Content value. Type: float(9,2)
customsCode	string	optional	200	Сustoms сode
country	string	optional	DE	Country of origin
}	object	optional
Contents Items {object} block end
]	array	optional
Contents Items [array] block end
codPaymentsItems	array	optional
COD Payments Items [array] with {object}s block
[	array	optional
COD Payments Items [array] block start
{	object	optional
COD Payments Items {object} block start
agentId	string	required	546234532	EDRPOU of the recipient of funds                ----  -- -- ----
cod	number($float)	required	1200	The amount of funds from the total COD          --- -- -- -- ---
}	object	optional
COD Payments Items {object} block end
]	array	optional
COD Payments Items [array] block end
goods	array	optional
Goods [array] with {object}s block
[	array	optional
Goods [array] block start
{	object	optional
Goods {object} block start
article	string	required	651-24523	article                                         - -- --- ------
name	string	required	monitor	name                                                --- - ---- ----

weight	number($float)	required	12	Weight                                        ---  ------- --
quantity	integer($int32)	required	2	Quantity                                      --- ----- -- --
price	number($float)	required	8700	Price                                         - -- ---- - ---
length	number($float)	optional	130	Lenght
width	number($float)	optional	25	Width
height	number($float)	optional	75	Height
}	object	optional
Goods {object} block end
]	array	optional
Goods [array] block end
}	object	required                                                                 ------------
Main {object} block end
"""

mees_parcel = {
    'parcelNumber':	'',  # %%%% optional	TST-2550636	Shipment number
    'notation':	'',  # %%%% optional	notation	Notation, comment
    'payType': 'noncash',   # required	cash	Payment type. Options: cash, noncash
    # required	false Who pays for the shipment. «False» - Sender, «true» - Receiver
    'receiverPay':	False,
    # optional	19.03.2019	Shipment date. If this parameter is empty,
    # the “estimatedDeliveryDate” parameter will not be calculated in the response.
    # Format: dd.MM.yyyy
    'sendingDate':	"19.03.2019",
    'sender': {
                'name':	 "string",  # required	Dawn Lyons	Sender name
                'phone': "string",  # required	+1-202-555-0171	Sender phone
                'zip':   'string',  # optional	12601	Sender postal code
                # %%%% string	required	328a79e5-8452-11e8-80d4-1c98ec135261
                # Unique sender Branch ID identifier.
                # Obtained by “branchSearch” function. Required if service == Branch
                'branchID': '328a79e5-8452-11e8-80d4-1c98ec135261',
                'service': 'Branch',  # Delivery type options: Door, Branch
    },
    'receiver': {
        'name':	'Peter Peterson	Receiver',  # required	Peter Peterson	Receiver name
        'phone':	'string',                 # required	+380920639860	Receiver phone
        'zip':	'string',  # required	98891	Receiver postal code
        # required	6e23d513-e0d2-11df-9b37-00215aee3ebe	Unique receiver Address ID.
        # Obtained by “addressSearch” function. Required if service == Door
        'addressID':	'6e23d513-e0d2-11df-9b37-00215aee3ebe',
        # required	50	Receiver building number. Required if service == Door
        'building':	'string',
        'flat':	'122',  # ??? %%%% string	# optional	122	Receiver flat number
        'floor': 1,  # %%%% integer($int32)	optional	8	Receiver floor number
        'service':	'Door',  # -  required	Branch	Delivery type. Options: Door, Branch
    },  # -  object	required

    # %%%% 'placesItems' - ширина/длина/высота/ название объекта - или описание/комментарий
    # %%%%%%  -  placesItems	array	required  Places Items [array] with {object}s block
    'contentsItems': [
        {  # -  Places Items {object} block start
            'contentName': "Поліграфія",  # %%%% -  string	required	trouses	Content name
            'serialNumber': " ",  # %%%%  string	optional	SN34943516546546	Serial Number % % % %
            'quantity':	1,  # required	1	Places quantity
            'weight': -1,  # number($float)      # - 	required	0.589	Weight, kg. Type: float(8,3)
            'volume': -3.62,  # number($float)  optional	5.121	Volume. Type: float(7, 3)
            # number   ($float)	optional	200	Declared value of shipping. Type: float(9, 2)
            'insurance': -100,
            # %%%%   optional	c26956ba-a2ce-11e4-b90b-003048d2b473
            # Unique pack ID. Obtained by “packTypes” function
            'packID':	' ',
            # %%%%%%%%%%%%%%%%%%%%%%% integer($int32) - -- -- -- -  optional	20	Length, cm
            'length': -20,
            'width': -20,  # %%%% 	integer($int32) optional	30	Width, cm
            'height': -20,  # %%%%   integer($int32)  optional	10	Height, cm
        },
    ]
}


mees_parcel = {
    'parcelNumber':	'',
    'notation':	'',
    'payType': 'noncash',
    'receiverPay':	False,
    'sendingDate':	"19.03.2019",
    'sender': {
                'name':	 "string",
                'phone': "+380504522559",
                'zip':   '49050',
                'branchID': '328a79e5-8452-11e8-80d4-1c98ec135261',
                'service': 'Branch',
    },
    'receiver': {
        'name':	'Peter Peterson	Receiver',
        'phone':	'string',
        'zip':	'string',
        'addressID':	'6e23d513-e0d2-11df-9b37-00215aee3ebe',
        'building':	'string',
        'flat':	'122',
        'floor': 1,
        'service':	'Door',
    },

    'contentsItems': [
        {
            'contentName': "Поліграфія",
            'serialNumber': " ",
            'quantity':	1,
            'weight': 1,
            'volume': 0.362,

            'insurance': 100,
            'packID':	' ',
            'length': 20,
            'width': 20,
            'height': 20,
        },
    ]
}


mees_parcel = {
    'notation':	'Коментар',
    'payType': 'noncash',
    'receiverPay':	False,
    'sendingDate':	"07.12.2021",
    'sender': {
                'name':	 "string",
                'phone': "+380504522559",
                'zip':   '49050',
                'branchID': '328a79e5-8452-11e8-80d4-1c98ec135261',
                'service': 'Branch',
    },
    'receiver': {
        'name':	'Peter Peterson	Receiver',
        'phone':	'string',
        'zip':	'string',
        'addressID':	'6e23d513-e0d2-11df-9b37-00215aee3ebe',
        'building':	'string',
        'flat':	'122',
        'floor': 1,
        'service':	'Door',
    },

    'contentsItems': [
        {
            'contentName': "Поліграфія",
            'serialNumber': " ",
            'quantity':	1,
            'weight': 1,
            'volume': 0.362,

            'insurance': 100,
            'packID':	' ',
            'length': 20,
            'width': 20,
            'height': 20,
        },
    ]
}


"""
curl --location --request POST 'https://api.meest.com/v3.0/openAPI/parcel' \
--header 'token: ab63a1cf6cfad861187617c14bb4ce26' \
--header 'Content-Type: application/json' \
--data-raw '{
    "receiverPay": false, // платить відправник
    "cod": 600,  // це сод(післяплата)
    "notation": "коментар який буде надрукований на накладній", // коментар
    "sender": {
        "phone": "380965231700",
        "name": "test",
        "service": "Door",
        "addressID": "bfd6e795-e0d4-11df-9b37-00215aee3ebe" // тут унікальний ідентифікатор адреси отримати який можна в функції addressSearch
    },
    "placesItems": [
        {
            "weight": 0.001,
            "height": 0,
            "width": 0,
            "length": 0,
            "insurance": 0.0,
            "quantity": 1
        }
    ],
    "receiver": {
        "name": "Петро mariyuchin",
        "phone": "+380965231700",
        "service": "Door",
        "addressId": "bfd6e795-e0d4-11df-9b37-00215aee3ebe", // тут унікальний ідентифікатор адреси отримати який можна в функції addressSearch
        "building": "50",
        "flat": "112",
        "floor": "8"
    },
    "payType": "noncash"  // безготівка
}'
"""

{
    "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
    "receiverPay": False,
    "cod": 600,
    "notation": "коментар який буде надрукований на накладній",
    "sender":
        {"phone": "380965231700",
         "name": "test",
         "service": "Door",
         "addressID": "fdca4394-eda1-11df-b61a-00215aee3ebe",
         "building": "10",
         "flor": "1"
         },
    "placesItems": [
            {"weight": 0.101,
             "height": 5,
             "width":  4,
             "length": 7,
             "insurance": 10.0,
             "quantity": 1,
             }
        ],
    "receiver": {
        "name": "Ган Зоряна Анатоліївна",
        "phone": "380678311104",
        "service": "Door",
        "addressID": "62c3d54a-749b-11df-b112-00215aee3ebe",
        "building": "41",
        "flat": "1",
        "floor": "1",
        },

    "payType": "noncash",
}

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
