
import abc

from collections import namedtuple
import requests
import json

from datetime import datetime as dt, timedelta

from settings import credentials


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
    Registers = namedtuple('Registers', ['create', 'edit', 'delete'])
    Print = namedtuple('Print', ['sticker100', 'sticker100_A4', 'registers', 'declarations'])
    Tracking = namedtuple('Tracking', ['method', ])

    # instances = {}  # Singleton-like  # TODO: del

    def __init__(self, post_service_credentials: dict) -> None:
        self.url = post_service_credentials['url']
        self.content_type = {'Content-Type': 'application/json'}  # const for header
        # "a3df71d8-5e17-11ea-80c6-000c29800ae7"
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

        response = self._do_auth(post_service_credentials)
        self._get_auth_result(response)
        

    # =============================================================================================
    # AUTH functions block
    #
    @abc.abstractmethod
    def _do_auth(self, post_service_credentials: dict) -> dict:
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


class APINovaPoshta(PostServiceLight):
    
    def __init__(self, post_service_credentials):
        super().__init__(post_service_credentials)
              
    # =============================================================================================
    # AUTH functions block
    #

    def _do_auth(self, post_service_credentials: dict) -> dict:
        self.auth_response_code = post_service_credentials['apiKey']

    def _get_auth_result(self, resp):
        #TODO нет в новой почте
        return 0

    def authotize_refresh_token(self):
        #TODO нет в новой почте
        return 0

    # =============================================================================================
    # PARCELS functions block
    #

    def _create_parcell(self, **kwargs):
       
       # kwargs ------
       
       # {'PayerType': "Sender",
       #  'PaymentMethod': "Cash",
       #  'DateTime': "02.03.2015",
       #  'CargoType': "Cargo",
       #  'VolumeGeneral': "0.1",
       #  'Weight': "10",
       #  'ServiceType': "WarehouseDoors",
       #  'SeatsAmount': "1",
       #  'Description': "абажур",
       #  'Cost': "500",
       #  'CitySender': "8d5a980d-391c-11dd-90d9-001a92567626",
       #  'Sender': "6e9acced-d072-11e3-95eb-0050568046cd",
       #  'SenderAddress': "01ae2635-e1c2-11e3-8c4a-0050568002cf",
       #  'ContactSender': "d0b9f592-b600-11e4-a77a-005056887b8d",
       #  'SendersPhone': "380678734567",
       #  'CityRecipient': "db5c8892-391c-11dd-90d9-001a92567626",
       #  'Recipient': "d00f2319-b743-11e4-a77a-005056887b8d",
       #  'RecipientAddress': "511fcfbd-e1c2-11e3-8c4a-0050568002cf",
       #  'ContactRecipient': "bc7b61ea-b6eb-11e4-a77a-005056887b8d",
       #  'RecipientsPhone': "380631112223" }
       
       props = {k: v for k, v in kwargs.items() if v}
            
       data = {
            'apiKey': self.auth_response_code,
            'modelName': 'InternetDocument',
            'calledMethod': 'save',
            'methodProperties': props
            }
    
       response = requests.post(self.url, json=data, headers=self.content_type)
       ref = json.loads(response.content)['data']
               
       return response.status_code, ref


    def _get_parcells_list_on_date(self, date: str = '13.12.2021'):
        
        data = {
            'apiKey': self.auth_response_code,
            'modelName': 'InternetDocument',
            'calledMethod': 'getDocumentList',
            'methodProperties': {'DateTimeFrom': date,
                                 'DateTimeTo': date,
                                 'Page': 1,
                                 'GetFullList': 0
                                 }
            }
    
        response = requests.post(self.url, json=data, headers=self.content_type)
        ref = json.loads(response.content)['data']
               
        return response.status_code, ref


    def _del_parcell_by_id(self, parcel_id: str = ''):
        
        data = {
            'apiKey': self.auth_response_code,
            'modelName': 'InternetDocument',
            'calledMethod': 'delete',
            'methodProperties': {'DocumentRefs': parcel_id,
                                 }
            }
    
        response = requests.post(self.url, json=data, headers=self.content_type)
        ref = json.loads(response.content)['data']
               
        return response.status_code, ref

    # =============================================================================================
    # SEARCH functions block
    #

    def _branch_ID_search(self, city_id: str, branch_number: str):  # 'branchSearchGeo'
        data = {
            'apiKey': self.auth_response_code,
            'modelName': "Address",
            'calledMethod': "getWarehouses",
            'methodProperties': {
                                'CityName': city_id,
                                'FindByString': branch_number
                                }
            }
    
        response = requests.post(self.url, json=data, headers=self.content_type)
        rezdate = json.loads(response.content)['data']
        if len(rezdate) != 0:
            ref = rezdate[0]['Ref']
        else:
            ref = 0 
        
        return response.status_code, ref


    def _city_by_ZIP_search(self, zipCode: str = '49055'):
        data = {
                'apiKey': self.auth_response_code,
                'modelName': "Address",
                'calledMethod': "searchSettlements",
                'methodProperties': {
                                    'CityName': zipCode,
                                    'Limit': 1
                                    }
                }
        
        response = requests.post(self.url, json=data, headers=self.content_type)
        rezdate = json.loads(response.content)['data'][0]
        if len(rezdate['Addresses']) != 0:
            ref = rezdate['Addresses'][0]['Ref']
        else:
            ref = 0

        return response.status_code, ref
        

    def _city_by_ukr_name_search(self, city_descr: str,
                                  region_descr: str = None,  # Область
                                  ):
        data = {
                'apiKey': self.auth_response_code,
                'modelName': "Address",
                'calledMethod': "getCities",
                'methodProperties': {
                                    'FindByString': city_descr,
                                    'Page': 1
                                    }
                }
        
        response = requests.post(self.url, json=data, headers=self.content_type)
        rezdate = json.loads(response.content)['data']
        if len(rezdate) != 0:
            ref = rezdate[0]['Ref']
        else:
            ref = 0      
        return response.status_code, ref


    def _address_by_streetname_search(self, city_id: str = '', streetname: str = ''):
        data = {
            'apiKey': self.contract_id,
            'modelName': "Address",
            'calledMethod': "searchSettlementStreets",
            'methodProperties': {
                                'StreetName': streetname,
                                'SettlementRef': city_id,
                                'Limit': 1
                                }
            }
    
        response = requests.post(self.url, json=data, headers=self.content_type)
        rezdate = json.loads(response.content)['data'][0]
        
        if len(rezdate['Addresses']) != 0:
            ref = rezdate['Addresses'][0]['SettlementStreetRef']
        else:
            ref = 0
            
        return response.status_code, ref 

    # =========================================================================================
    # PRINT functions block
    # 

    def _print_sticker100(self, parcels_IDs_list: list = []):
        return 0

    def _print_sticker100_A4(self, parcels_IDs_list: list = []):
        return 0


if __name__ == "__main__":
    
    API = APINovaPoshta(credentials["post_service_credentials"])
        
    # ref = API._city_by_ZIP_search("21012")
    # ref = API._city_by_ukr_name_search('Вінниця')
    # ref = API._branch_ID_search("Вінниця", "Відділення №26") 
    # ref = API._address_by_streetname_search(API._city_by_ZIP_search("21012"), "Пирогова")
    # ref = API._get_parcells_list_on_date("31.12.2021")
    # ref = API._del_parcell_by_id("31.12.2021")
    
    ref = API._create_parcell(PayerType="Sender",
       PaymentMethod="Cash",
       DateTime="02.03.2015",
       CargoType="Cargo",
       VolumeGeneral="0.1",
       Weight="10",
       ServiceType="WarehouseDoors",
       SeatsAmount="1",
       Description="абажур",
       Cost="500",
       CitySender="8d5a980d-391c-11dd-90d9-001a92567626",
       Sender="6e9acced-d072-11e3-95eb-0050568046cd",
       SenderAddress="01ae2635-e1c2-11e3-8c4a-0050568002cf",
       ContactSender="d0b9f592-b600-11e4-a77a-005056887b8d",
       SendersPhone="380678734567",
       CityRecipient="db5c8892-391c-11dd-90d9-001a92567626",
       Recipient="d00f2319-b743-11e4-a77a-005056887b8d",
       RecipientAddress="511fcfbd-e1c2-11e3-8c4a-0050568002cf",
       ContactRecipient="bc7b61ea-b6eb-11e4-a77a-005056887b8d",
       RecipientsPhone="380631112223")
    print(ref)
