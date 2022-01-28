"""[summary]

 Ширина, Довгота:  48.44, 35.06
Returns:
    [type]: [description]
"""
import abc

from collections import namedtuple
import requests
import json

from pprint import pprint

from datetime import datetime as dt
from datetime import timedelta, date

from settings import credentials


def tomorrow() -> str:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return tomorrow.strftime('%d.%m.%Y')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PostServiceLight(abc.ABC):
    """[summary]
    """
    AuthorizationData = namedtuple('Auth', ['token', 'expire_time', 'refresh_token'])
    # methods packs:
    Search = namedtuple('Search', ['by_zip_city_id', 'by_ukr_name_city_id',
                                   'address_id',
                                   'branch_id',
                                   ])
    Parcels = namedtuple('Parcels', ['create', 'get_all_on_date', 'delete_by_id'])
    Registers = namedtuple('Registers', ['create_pick_up',
                           'edit_pick_up', 'delete_pick_up', 'get_all_on_date'])
    Print = namedtuple('Print', ['sticker100', 'sticker100_A4', 'registers', 'declarations'])
    Tracking = namedtuple('Tracking', ['method', ])

    # instances = {}  # Singleton-like  # TODO: del

    def __init__(self, post_service_credentials: dict) -> None:
        self.url = post_service_credentials['url']
        # const for header
        self.content_type = {'Content-Type': post_service_credentials['content_type']}
        self.username = post_service_credentials["username"]
        self.password = post_service_credentials["password"]
        self.contract_id = post_service_credentials['contract_id']

        self.headers = None
        self.auth_response_code = None
        self.authotize_data = None

        self.parcels = self.__class__.Parcels(
            create=self._create_parcell,
            get_all_on_date=self._get_parcells_list_on_date,
            delete_by_id=self._del_parcell_by_id,
        )
        self.search = self.__class__.Search(
            by_zip_city_id=self._city_by_ZIP_search,            # id міста за поштовим індексом
            by_ukr_name_city_id=self._city_by_ukr_name_search,  # id міста за українською назвою
            # id вулиці за українською назвою та id міста
            address_id=self._address_by_streetname_search,
            branch_id=self._branch_ID_search,                   # id відділення #TODO: за чим?
        )
        self.to_print = self.__class__.Print(
            sticker100=self._print_sticker100,         # друк у pdf-файл sticker100 стрічкою
            sticker100_A4=self._print_sticker100_A4,   # друк у pdf-файл sticker100 форматами А4
            registers=None,
            declarations=None,
        )

        self.register = self.__class__.Registers(
            create_pick_up=self._create_pickup_register,
            edit_pick_up=None,
            delete_pick_up=None,
            get_all_on_date=self._get_registers_list_on_date
        )

        response = self._do_auth()
        self._get_auth_result(response)

    # =============================================================================================
    # AUTH functions block
    #
    @abc.abstractmethod
    def _do_auth(self) -> dict:
        ...

    @abc.abstractmethod
    def _get_auth_result(self, resp):
        ...

    @abc.abstractmethod
    def authotize_refresh_token(self):
        ...

    # =============================================================================================
    # PARCELS functions block
    #

    @abc.abstractmethod
    def _create_parcell(self, **kwargs):
        ...

    @abc.abstractmethod
    def _get_parcells_list_on_date(self, date: str = '13.12.2021'):
        ...

    @abc.abstractmethod
    def _del_parcell_by_id(self, parcel_id: str = ''):
        ...

    # =============================================================================================
    # SEARCH functions block
    #

    @abc.abstractmethod
    def _branch_ID_search(self, city_id: str, branch_number: str):  # 'branchSearchGeo'
        ...

    @abc.abstractmethod
    def _city_by_ZIP_search(self, zipCode: str = '49055'):
        ...

    @abc.abstractmethod
    def _city_by_ukr_name_search(self, city_descr: str,
                                 region_descr: str = None,  # Область
                                 ):
        ...

    @abc.abstractmethod
    def _address_by_streetname_search(self, city_id: str = '', streetname: str = ''):
        ...

    # =========================================================================================
    # PRINT functions block
    #

    @abc.abstractmethod
    def _print_sticker100(self, parcels_IDs_list: list = []):
        ...

    @abc.abstractmethod
    def _print_sticker100_A4(self, parcels_IDs_list: list = []):
        ...

    def __str__(self):
        return F"class <{self.__class__}> has auth response code: {self.auth_response_code}"


class Postman(PostServiceLight):  # metaclass=Singleton
    """[summary]
    """
    # instances = {}  # Singleton-like  # TODO: del

    def __init__(self, credentials: dict) -> None:
        ##### TODO: rework
        super().__init__(credentials)
        self.sender = {
            "phone":  "+38050-421-1558",
            "name": "Васина Лариса",
            "service": "Door",
            "addressID": "d3d482e3-ed9f-11df-b61a-00215aee3ebe",
            "building": "10А",
            "floor": 1,
            "notation": "Типографія Арт-Прес, м. Дніпро",
        }

    # =============================================================================================
    # AUTH functions block
    #

    def _do_auth(self):
        response = requests.post(
            url="/".join([self.url, 'auth']),
            headers=self.content_type,
            json={
                "username": self.username,
                "password": self.password,
            },
        )
        return response

    def _get_auth_result(self, resp):
        self.auth_response_code = resp.status_code
        content_result = json.loads(resp.content)['result']
        self.authotize_data = self.__class__.AuthorizationData(
            token=content_result.get('token', None),
            expire_time=dt.now() + timedelta(seconds=int(content_result.get('expiresIn', 0))),
            refresh_token=content_result.get('refreshToken', None),
        )
        self.headers = {**self.content_type, 'token': self.authotize_data.token}

    def authotize_refresh_token(self):
        response = requests.post(
            url="/".join([self.url,  'refreshToken']),
            headers=self.headers,
            json={"refreshToken": self.authotize_data.refresh_token, },
        )
        self.__get_auth_result(response)
        return response.status_code

    # =============================================================================================
    # PARCELS functions block
    #

    def _create_parcell(self, **kwargs):
        json_body = {
            "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
            "receiverPay": False,
            # "COD": 600,
            "sendingDate": kwargs.get('sendingDate', tomorrow()),
            "notation": ".......",
            "sender": {
                "phone": kwargs.get('sender_phone', "+38050-421-1558"),
                "name": kwargs.get('sender_name', 'Васина Лариса'),
                "service": "Door",
                "addressID": "d3d482e3-ed9f-11df-b61a-00215aee3ebe",
                "building": "10А",
                "floor": 1,
                "notation": "Типографія Арт-Прес, м. Дніпро",
            },

            "placesItems": kwargs["placesItems"],
            # [
            #        {"weight": kwargs['weight'],
            #         "height": kwargs.get('height', 0.01),
            #         "width":  kwargs.get('width', 0.01),
            #         "length": kwargs.get('length', 0.01),
            #         "insurance": 500.0,
            #         "quantity": kwargs.get('quantity', 1),
            #         "notation": "Комментарий по placesItems",
            #         }
            #    ],

            "receiver": kwargs["receiver"],
            # {  # TODO:  form and gives dictionary here &&?
            #    "name": kwargs['name'],                                # 9
            #    "phone": kwargs['phone'],                              # 10
            #    "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",
            #    "zipCode": kwargs['zipCode'],                          # 11
            #    "addressID": kwargs['addreeID'],                       # 12
            #    "building": kwargs['buikding'],                        # 13
            #    "flat": kwargs.get('flat', "1"),
            #    "floor": kwargs.get('floor', 1),  # 15
            #    "service": "Door",
            # },

            "payType": "noncash",
        }

        if 'weight' in kwargs:
            json_body['weight'] = kwargs['weight']

        if 'contentsItems' in kwargs:
            json_body['contentsItems'] = kwargs["contentsItems"],
            # [
            #    {
            #        'contentName': kwargs['contentName'],
            #        'quantity':	1,
            #        'weight': 0.101,
            #        'value': 0.362,
            #    },
            # ],

        response = requests.post(
            url="/".join([self.url, 'parcel']),
            headers=self.headers,
            json=json_body)

        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        return response.status_code, content_result

    def _del_parcell_by_id(self, parcel_id: str = ''):
        """
        Delete parcel on parcelID.

        :param this: DESCRIPTION, defaults to 'parcel'
        :param parcel_id: DESCRIPTION, defaults to ''
        :type parcel_id: str, optional
        :return: DESCRIPTION
        :rtype: TYPE

        {
          "status": "ok",
          "info": {
            "fieldName": "",
            "message": "",
            "messageDetails": ""
          },
          "result": {}
        }
        """
        response = requests.delete(
            url="/".join([self.url, 'parcel', parcel_id, self.contract_id]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        return response.status_code, content_result

    def _get_parcells_list_on_date(self, date: str = '13.12.2021'):
        """
        Get parcells list opened in date.

        :param this: DESCRIPTION, defaults to 'parcelsList'
        :param date: DESCRIPTION, defaults to ''
        :type date: str, optional
        :return: DESCRIPTION
        :rtype: TYPE

        {
          "status": "ok",
          "info": {
            "fieldName": "",
            "message": "",
            "messageDetails": ""
          },
          "result": [
            {
              "parcelID": "4a430ffd-6b7d-11e2-a79e-003048d2b473",
              "parcelNumber": "TAC-2550636",
              "вarCode": "TAC-2550636",
              "registerID": "0750fc9e-7eac-11e9-80e0-1c98ec135261",
              "registerType": "registerPickUP"
            }
          ]
        }
        """
        response = requests.get(
            url="/".join([self.url, 'parcelsList', date]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        return response.status_code, content_result
    # =============================================================================================
    # SEARCH functions block
    #

    def _branch_ID_search(self, city_id: str, branch_no: int):
        """
        curl --location --request POST 'https://api.meest.com/v3.0/openAPI/branchSearch' \
        --header 'Content-Type: application/json' \
        --header 'token: 5c3749e3598ef423b092b7daf8405206' \
        --data-raw '{
            "filters": {
                "branchTypeID": "0c1b0075-cd44-49d1-bd3e-094da9645919",
                "branchNo": 	integer,  # ($int32)
                "cityID": "62c3d54a-749b-11df-b112-00215aee3ebe",
                "cityDescr": "Lviv%",
                "districtID": "8a199cde-41b9-11df-907f-00215aee3ebe",
                "districtDescr": "Lviv%",
                "regionID": "d15e3024-60b0-11de-be1e-0030485903e8",
                "regionDescr": "Lviv%"
            }
        }'


        response example:
        {
          "status": "OK",
          "info": {
            "fieldName": "",
            "message": "",
            "messageDetails": ""
          },
          "result": [
            {
              "branchID": "75ec298e-a8dd-11de-bac3-0030485903e8",
              "branchIDref": "0xBAC30030485903E811DEA8DD75EC298E",
              "branchNo": 4,
              "branchType": "ОВ",
              "branchTypeID": "0c1b0075-cd44-49d1-bd3e-094da9645919",
              "branchTypeDescr": "Відділення. Без обмежень ваги.",
              "branchTypeAPP": "1",
              "branchDescr": {
                "descrUA": "Львів (HUB)",
                "descrSearchUA": "Львів вул. Пасіки Зубрицькі (Заводська),56"
              },
              "addressID": "937c9e10-5517-11e9-80df-1c98ec135261",
              "addressDescr": {
                "descrUA": "вул. Пасіки Зубрицькі (Заводська)",
                "descrRU": "ул. Пасіки Зубрицькі",
                "descrEN": "Pasiky Zubrytski (Zavodska) st."
              },
              "addressMoreInformation": "",
              "cityID": "62c3d54a-749b-11df-b112-00215aee3ebe",
              "cityDescr": {
                "descrUA": "Львів",
                "descrRU": "Львов",
                "descrEN": "Lviv"
              },
              "districtID": "8a199cde-41b9-11df-907f-00215aee3ebe",
              "districtDescr": {
                "descrUA": "Львів",
                "descrRU": "Львов",
                "descrEN": "Lviv"
              },
              "regionID": "d15e3024-60b0-11de-be1e-0030485903e8",
              "regionDescr": {
                "descrUA": "ЛЬВІВСЬКА",
                "descrRU": "ЛЬВОВСКАЯ",
                "descrEN": "LVIVS`KA"
              },
              "workingHours": "Пн-Пт 09:00-19:00, Сб 09:00-15:00, Нд --:-----:--",
              "building": "56",
              "zipCode": "79019",
              "latitude": 49.778984,
              "longitude": 24.092983,
              "branchWorkTime": [
                {
                  "day": "Пн",
                  "timeFrom": "09:00",
                  "timeTo": "19:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Вт",
                  "timeFrom": "09:00",
                  "timeTo": "19:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Ср",
                  "timeFrom": "09:00",
                  "timeTo": "19:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Чт",
                  "timeFrom": "09:00",
                  "timeTo": "19:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Пт",
                  "timeFrom": "09:00",
                  "timeTo": "19:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Сб",
                  "timeFrom": "09:00",
                  "timeTo": "15:00",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                },
                {
                  "day": "Нд",
                  "timeFrom": "",
                  "timeTo": "",
                  "LunchBreakFrom": "",
                  "LunchBreakTo": ""
                }
              ],
              "phone": "(032)2452347",
              "address": "Львів вул. Пасіки Зубрицькі (Заводська),56",
              "paymentTypes": "",
              "branchLimits": {
                "weightTotalMax": 0,
                "volumeTotalMax": 0,
                "insuranceTotalMax": 0,
                "weightPlaceMax": 0,
                "quantityPlacesMax": 0,
                "gabaritesMax": {
                  "length": 0,
                  "width": 0,
                  "height": 0
                },
                "formatLimit": false,
                "cashPayUnavailible": false,
                "sendingOnly": true,
                "receivingOnly": true,
                "receiverCellPhoneRequired": false,
                "terminalCash": false
              }
            }
          ]
        }
        """

        response = requests.get(
            "/".join([self.url, 'branchSearch']),
            headers=self.headers,
            json={
                "filters": {
                    "branchNo": 	branch_no,  # ($int32)
                    "cityID": city_id,
                    "countryDescr": "UKR%",
                }}
        )
        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']

        if content_result:
            result = {"branchID": content_result[0]["branchID"],
                      "branchTypeDescr": content_result[0]["branchTypeDescr"],
                      "branchDescr": content_result[0]["branchDescr"],
                      }
        else:
            result = {"branchID": None}

        return response.status_code, result

    def _city_by_ZIP_search(self, zipCode: str = '49055'):
        """

        """
        response = requests.get(
            "/".join([self.url, 'zipCodeSearch', zipCode]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']

        # return response.status_code, content_result
        return response.status_code, content_result

    def _city_by_ZIP_search_first(self, zipCode: str = '49055'):
        """

        (200,
         [{'cityDescr': {'descrEN': 'Dnipro', 'descrRU': 'Днепр', 'descrUA': 'Дніпро'},
           'cityID': '50c5951b-749b-11df-b112-00215aee3ebe',
           'countryID': 'c35b6195-4ea3-11de-8591-001d600938f8',
           'deliveryDays': {'Fri': True,
                            'Mon': True,
                            'Sat': True,
                            'Sun': False,
                            'Thu': True,
                            'Tue': True,
                            'Wed': True},
           'deliveryZone': '1',
           'districtDescr': {'descrEN': 'Dnipro',
                             'descrRU': 'Днепро',
                             'descrUA': 'Дніпро'},
           'districtID': 'd00d3b5d-41b9-11df-907f-00215aee3ebe',
           'isBranchInCity': True,
           'regionDescr': {'descrEN': 'DNIPROPETROVS`KA',
                           'descrRU': 'ДНЕПРОПЕТРОВСКАЯ',
                           'descrUA': 'ДНІПРОПЕТРОВСЬКА'},
           'regionID': 'd15e301b-60b0-11de-be1e-0030485903e8',
           'zipCode': '49055'}])

        """
        status_code, content_result = self.__city_by_ZIP_search(
            this='zipCodeSearch', zipCode=zipCode)

        return "_".join([str(len(content_result)), content_result[0]['cityID']])

    def _city_by_ZIP_wise_pick(self, responsed_list: list = list(),
                               city_name: str = 'Дніпро', zipCode: str = '49055',  # Ukraine ID:
                               countryID: str = 'c35b6195-4ea3-11de-8591-001d600938f8',
                               ):

        multi_to_choice = list()
        if len(responsed_list) == 1:
            return (responsed_list[0]['cityID'], responsed_list[0]['cityDescr']['descrUA'])
        for city_dict in responsed_list:
            if (city_name in city_dict['cityDescr']['descrUA']
                    and countryID == city_dict['countryID']):
                return (city_dict['cityID'], city_dict['cityDescr']['descrUA'])
            else:
                # TODO: ONLY UKRAINIAN CITY NAME
                multi_to_choice.append({'cityDescrUA': city_dict['cityDescr']['descrUA'],
                                        'cityID': city_dict['cityID']},
                                       )
        else:
            return multi_to_choice

    def _city_by_ukr_name_search(self, city_descr: str = None,
                                 region_descr: str = None,  # Область
                                 country_id: str = 'c35b6195-4ea3-11de-8591-001d600938f8',
                                 ):
        '''
        curl --location --request POST 'https://api.meest.com/v3.0/openAPI/citySearch' \
        --header 'Content-Type: application/json' \
        --header 'token: 5c3749e3598ef423b092b7daf8405206' \
        --data-raw '{
            "filters": {
                "cityDescr": "Lviv%",
                "districtDescr": "Lviv%",
                "regionDescr": "Lviv%",
                "countryDescr": "UKR%"
            }
        }'



        {
          "status": "OK",
          "info": {
            "fieldName": "",
            "message": "",
            "messageDetails": ""
          },
          "result": [
            {
              "cityID": "62c3d54a-749b-11df-b112-00215aee3ebe",
              "cityKATUU": "4610100000",
              "cityDescr": {
                "descrUA": "Львів",
                "descrRU": "Львов",
                "descrEN": "Lviv"
              },
              "districtID": "8a199cde-41b9-11df-907f-00215aee3ebe",
              "districtDescr": {
                "descrUA": "Львів",
                "descrRU": "Львов",
                "descrEN": "Lviv"
              },
              "regionID": "d15e3024-60b0-11de-be1e-0030485903e8",
              "regionDescr": {
                "descrUA": "ЛЬВІВСЬКА",
                "descrRU": "ЛЬВОВСКАЯ",
                "descrEN": "LVIVS`KA"
                "cityDescr": city_descr + "%",  # "Lviv%",
              },
              "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",
              "isBranchInCity": true,
              "deliveryZone": "1",
              "deliveryDays": {
                "Mon": true,
                "Tue": true,
                "Wed": true,
                "Thu": true,
                "Fri": true,
                "Sat": true,
                "Sun": false
              },
              "latitude": 49.839678,
              "longitude": 24.029709
            }
          ]
        }

        '''
        send_json = {
            "filters": {
                #  "districtDescr": "Lviv%",
                #  "regionDescr": "Lviv%",
                "cityDescr": city_descr,
                "countryID": country_id,
            }}

        if region_descr:
            json["filters"]["regionDescr"] = region_descr

        response = requests.post(
            url="/".join([self.url, 'citySearch']),
            headers=self.headers,
            json=send_json,
        )

        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        return response.status_code, content_result

    def _city_by_ukrname_wise_pick(
        self, responsed_list: list = list(),
            city_name: str = 'Дніпро',  # Ukraine ID:
            countryID: str = 'c35b6195-4ea3-11de-8591-001d600938f8',
    ):

        multi_to_choice = list()
        if len(responsed_list) == 1:
            return (responsed_list[0]['cityID'], responsed_list[0]['cityDescr']['descrUA'])

        for city_dict in responsed_list:
            if (city_name in city_dict['cityDescr']['descrUA']
                    and countryID == city_dict['countryID']):
                return (city_dict['cityID'], city_dict['cityDescr']['descrUA'])
            else:
                multi_to_choice.append(
                    {
                        'cityDescrUA': city_dict['cityDescr']['descrUA'],
                        'cityID': city_dict['cityID'],
                    }
                )
        else:
            return multi_to_choice

    def _address_by_streetname_search(self, city_id: str = '', streetname: str = ''):
        """
            POST request example:
            curl --location --request POST 'https://api.meest.com/v3.0/openAPI/addressSearch' \\
            --header 'Content-Type: application/json' \\
            --header 'token: 5c3749e3598ef423b092b7daf8405206' \\
            --data-raw '{
                "filters": {
                    "cityID": "62c3d54a-749b-11df-b112-00215aee3ebe",
                    "addressDescr": "%Gorodotska%"
                }
            }'


            Responce example:
            {
              "status": "OK",
              "info": {
                "fieldName": "",
                "message": "",
                "messageDetails": ""
              },
              "result": [
                {
                  "addressID": "d464524f-e0d3-11df-9b37-00215aee3ebe",
                  "addressDescr": {
                    "descrUA": "вул. Городоцька",
                    "descrRU": "ул. Городоцкая",
                    "descrEN": "Gorodotska st."
                  },
                  "cityID": "62c3d54a-749b-11df-b112-00215aee3ebe"
                }
              ]
            }


        """
        response = requests.post(
            "/".join([self.url, 'addressSearch']),
            headers=self.headers,
            json={"filters":
                  {
                      "cityID": city_id,                 # "62c3d54a-749b-11df-b112-00215aee3ebe",
                      "addressDescr": streetname.join(["%", "%"])       # "%Gorodotska%"
                  }
                  }
        )

        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        # return response.status_code, content_result
        return response.status_code, content_result

        # =========================================================================================
        # PRINT functions block
        #

    def _print_sticker100(self, parcels_IDs_list: list = []):
        """

        """
        response = requests.get(  # TODO: page=
            "/".join([self.url, r'print/sticker100', ",".join(parcels_IDs_list), "?page=2"]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = response.content   # not content['result']  - bc of stream result in

        # return response.status_code, content_result
        return response.status_code, content_result

    def _print_sticker100_A4(self, parcels_IDs_list: list = []):
        """

        """
        response = requests.get(
            "/".join([self.url, r'print/sticker100A4', ",".join(parcels_IDs_list)]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = response.content   # not content['result']  - bc of stream result in

        # return response.status_code, content_result
        return response.status_code, content_result

    def _create_pickup_register(self,
                                expected_pick_date=dict(
                                    date=tomorrow(),  # "20.01.2022"
                                    timeFrom="15:00",
                                    timeTo="18:00"),
                                sender=False,
                                parcels_tokens_list: list = []):
        """

        """
        json_body = {
            "contractID": self.contract_id,
            "payType": "noncash",
            "receiverPay": "false",
            "expectedPickUpDate": expected_pick_date,
            "sender": sender if sender else self.sender,
            "parcelsItems": [{"parcelId": token} for token in parcels_tokens_list]

        }
        response = requests.post(
            "/".join([self.url, 'registerBranch']),
            headers=self.headers,
            json=json_body,
        )
        self.auth_response_code = response.status_code
        content_result = response.content   # not content['result']  - bc of stream result in

        # return response.status_code, content_result
        return response.status_code, content_result

    def _get_registers_list_on_date(self, date: str = '13.12.2021'):
        """
        Get registers list opened in date.

        https://api.meest.com/v3.0/openAPI/print/register/25670e42-8045-11ec-80e4-000c29800ae7/pdf

        :param this: DESCRIPTION, defaults to 'parcelsList'
        :param date: DESCRIPTION, defaults to ''
        :type date: str, optional
        :return: DESCRIPTION
        :rtype: TYPE

         {
          "status": "ok",
          "info": {
            "fieldName": "",
            "message": "",
            "messageDetails": ""
          },
          "result": [
            {
              "registerID": "42aa64ae-81d2-11e9-80e0-1c98ec135261",
              "registerType": "registerPickUP",
              "parcelQty": 2
            }
          ]
        }
        """
        response = requests.get(
            url="/".join([self.url, 'registersList', date]),
            headers=self.headers,
        )
        self.auth_response_code = response.status_code
        content_result = json.loads(response.content)['result']
        return response.status_code, content_result

        #
        # MAGIC functions block
        #

    def __str__(self):
        return F"class <{self.__class__}> has auth response code: {self.auth_response_code}"


if __name__ == "__main__":
    postman = Postman(credentials['Meest'])
    print('1', postman)
    z = postman.authotize_data.token
    print(z)

    # postman.authotize_refresh_token()
    print('2', postman)

    # postman.parcels.delete_by_id()
    print('3', postman)

    # print(postman.search.branch_id())
    # print('4', postman)

# =============================================================================
#     print(postman.parcels.create())
#     print('5', postman)
# =============================================================================
# =============================================================================
#     code, pdf_bytes = postman.to_print.sticker100(
#         parcels_IDs_list=['04d1b81e-5818-11ec-80e4-000c29800ae7',
#                           'f74bc8e2-5817-11ec-80e4-000c29800ae7',
#                           '04d1b82a-5818-11ec-80e4-000c29800ae7',
#                           '17405cd4-5818-11ec-80e4-000c29800ae7',
#                           ])
#     print(code, pdf_bytes)
#     print('6', postman)
#
# =============================================================================

    code, pdf_bytes = postman.to_print.sticker100_A4(
        parcels_IDs_list=['8dc2992a-7f8a-11ec-80e4-000c29800ae7',
                          ])

# =============================================================================
#     print(code, pdf_bytes)
#     print('7', postman)
# =============================================================================

# =============================================================================
#     import base64
#
#     with open("my_file.pdf", 'wb') as f:
#         # f.write(base64.b64decode(pdf_bytes))
#         f.write(pdf_bytes)
#         f.write(pdf_bytes)
# =============================================================================
# =============================================================================
#     z = postman.search.by_zip_city_id('08703')  # 85302
#     print('8', end="")
#     pprint(z)
#
#     z = postman.search.address_id(
#         city_id='6ed8178d-749b-11df-b112-00215aee3ebe',
#         streetname="Київська"
#     )
#     print('9', end="")
#     pprint(z)
# =============================================================================

    z = postman.search.by_zip_city_id('32302')  # Індекс
    print('8', end="")
    pprint(z)

    city_id = z[1][0]['cityID']
    z = postman.search.address_id(
        city_id=city_id,
        streetname="Добрянс"
    )
    print('9:  -> ', end="")
    pprint(z)

    z = postman.search.by_ukr_name_city_id(city_descr="Лиманка")
    print('10', end="")
    pprint(z)

    code, z = postman.register.get_all_on_date(date="28.01.2022")
    print('10', end="")
    pprint(z)
