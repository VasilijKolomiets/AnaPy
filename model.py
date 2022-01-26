# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 15:39:36 2022

@author: Vasil
"""
from settings import from_server_connect
import ua_posts_api


def sql_connect_commit_close(f):
    def wrapper():
        global temp_cursor
        cnx = from_server_connect()
        temp_cursor = cnx.cursor()   # used inside f-function

        command_pattern = f()  # внутри f() - только команда SQLite была бы ...
        # temp_cursor.execute(command_pattern)  # SQL command executing
        cnx.commit()
        cnx.close()
    return wrapper


def select_fields_from_table(
        fields='id, company_name, short_name_latin',
        table='companies',
        where_condition='is_active'
):

    cnx = from_server_connect()
    _cursor = cnx.cursor()

    command_pattern = F'SELECT {fields} FROM {table} WHERE {where_condition}'
    _cursor.execute(command_pattern)  # SQL command executing

    selected_data = _cursor.fetchall()

    cnx.commit()
    cnx.close()
    return selected_data


def add_row_values_to_DB(tablename: str, fields_values: dict):

    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = 'INSERT INTO {table}({fields_list}) VALUES ({multi_ss})'
    # sql_command = command_pattern.format(", :".join([''] + list(_widgets.keys()))[2:])

    fileds, qs, values = zip(*[(k, " %s", v) for k, v in fields_values.items()])

    sql_command = command_pattern.format(
        table=tablename,
        fields_list=", ".join(fileds),
        multi_ss=", ".join(qs),
    )

    # SQL command executing
    _cursor.execute(sql_command, values)
    last_id = _cursor.lastrowid  # i.e. _cursor.execute('SELECT LAST_INSERT_ID()')

    cnx.commit()
    cnx.close()
    return last_id


def add_point_to_DB(_widgets):
    """Connect to BD and INSERT data."""
    # global temp_cursor
    """
    'id_receivers', 'int', 'NO', 'PRI',      NULL, 'auto_increment'
    'id_companies', 'int', 'NO', 'MUL',      NULL, ''
    'surname', 'varchar(45)', 'YES', '',     NULL, ''
    'name', 'varchar(45)', 'YES', '',        NULL, ''
    'middle_name', 'varchar(45)', 'YES', '', NULL, ''
    'phone', 'varchar(19)', 'YES', '',       NULL, ''
    'city', 'varchar(45)', 'YES', '',        NULL, ''
    'street', 'varchar(45)', 'YES', '',      NULL, ''
    'building', 'varchar(5)', 'YES', '',     NULL, ''
    'floor', 'int', 'YES', '',               NULL, ''
    'flat', 'varchar(45)', 'YES', '',        NULL, ''
    'comment', 'varchar(255)', 'YES', '',    NULL, ''
    'date_in', 'date', 'YES', '',            NULL, ''
    'branch', 'varchar(45)', 'YES', '',      NULL, ''
    'active', 'tinyint', 'YES', '',          '1', ''
    'post_ZIP', 'varchar(5)', 'YES', '',     NULL, ''

    """
    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = 'INSERT INTO receivers({fields_list}) VALUES ({multi_ss})'
    # sql_command = command_pattern.format(", :".join([''] + list(_widgets.keys()))[2:])
    sql_command = command_pattern.format(
        {
            'fields_list': ", ".join(list(_widgets.keys())),
            'multi_ss': (13*"%s, ")[:-2]
        })
    values = tuple(v['entry'].get() for k, v in _widgets.items())
    # SQL command executing
    _cursor.execute(sql_command, values)
    # clearing FORM to next input

    cnx.commit()
    cnx.close()


def add_row_to_handbook_nd_get_added_id(
        handbook_id=dict(name='id_cities', value=None),  # for get id if exists!
        filter_id=dict(name='postservice_id', value=None),
        token=dict(name='city_token', value=None),
        handbook_field=dict(name='city_name', value=None),
        # fields='postservice_id, city_name, city_token',
        table_in='cities',


) -> int:  # or None )
    """ `cities` fields:
        `id_cities`, `postservice_id`, `city_name`, `city_token`, `citiescol`


        `postman`.`streets` fields:
        `id_streets`, `city_id`, `street_name`, `street_token`

    """
    fields_ = F'{handbook_id["name"]}, {filter_id["name"]}, {token["name"]}'
    where_condition_ = F'''{filter_id["name"]}={filter_id["value"]}
                            and {token["name"]}="{token["value"]}"'''

    selected_by_token = select_fields_from_table(
        fields=fields_,
        table=table_in,
        where_condition=where_condition_
    )

    if selected_by_token:
        return selected_by_token[0][0]  # handbook_id
    elif token['value']:
        last_id = add_row_values_to_DB(
            table_in,
            {
                filter_id['name']: filter_id['value'],
                token['name']: token['value'],
                handbook_field['name']: handbook_field['value'],
            }
        )
        return last_id
    else:
        return None


def add_row_to_waybills_nd_get_added_id(  # TODO: !!!
        delivery_contracts_id=None,  # for get id if exists!
        waybills_receivers_id=None,
        to_insert: dict = dict(),
):
    """

    """
    table_in = 'contract_waybills'
    where_condition_ = F'''
    delivery_contracts_id={delivery_contracts_id}
    and waybills_receivers_id={waybills_receivers_id}'''

    selected_by_filter = select_fields_from_table(
        fields='id_waybills',
        table=table_in,
        where_condition=where_condition_
    )

    if selected_by_filter:
        return selected_by_filter[0][0]
    elif delivery_contracts_id and waybills_receivers_id:
        last_id = add_row_values_to_DB(
            table_in,
            to_insert,
        )
        return last_id
    else:
        return None


def get_items_id_by(
    delivery_contracts_id: int,  # delivery_id saved in DB table 'items'
    item_id_in_delivery: int,   # item_in_delivery_id saved in DB table 'items'
) -> int:                       # item_id returned from table 'items'
    """Get item id in DB table 'items' by delivery_id & item_id_in_delivery pair."""

    where_condition = F"delivery_contracts_id={delivery_contracts_id} and item_id_in_delivery={item_id_in_delivery}"
    item_id = select_fields_from_table(
        table='items', fields='id_items',
        where_condition=where_condition
    )[0][0]

    assert item_id, F"""get_items_id_by NOTHING FOUND by:
        {where_condition}...
        """
    return item_id


def get_rps_id_by(
        rps_postservices_id: int,  # postservices_id saved in DB table 'contract_waybills'
        waybills_receivers_id: int,  # receivers_id saved in DB table 'contract_waybills'
) -> int:
    where_condition = F"""rps_postservices_id={rps_postservices_id}
        and rps_receivers_id={waybills_receivers_id}"""
    id_rps = select_fields_from_table(
        table='receiver_postservice_street', fields='id_r_p_street',
        where_condition=where_condition
    )
    assert id_rps, F"Немає клієнта з таким ID {waybills_receivers_id}"
    return id_rps[0][0]


def get_if_street_building_surname_combo_id(
    rps_receivers_id=None,
    rps_postservices_id=None,
    rps_streets_id=None,
    building_to_check=None,
    name_to_check=None,
):
    """
    `receiver_postservice_street`  (rps)  fields:
        `id_r_p_street`, `rps_receivers_id`, `rps_postservices_id`, `rps_streets_id`

    returns:
        - None   if not found or
        - 'id_r_p_street' int value found
    """

    selected_by_token = select_fields_from_table(
        fields='id_receivers, id_r_p_street, rps_receivers_id, rps_postservices_id, rps_streets_id, receivers.surname, receivers.building',
        table='receivers LEFT JOIN receiver_postservice_street ON id_receivers=rps_receivers_id',
        where_condition=F"""
        rps_postservices_id = {rps_postservices_id} and rps_streets_id = {rps_streets_id}
        and receivers.surname = '{name_to_check}' and receivers.building = '{building_to_check}'
        """
    )

    if selected_by_token:
        return selected_by_token[0][0]  # handbook_id
    else:
        return None


def get_ordered_parcells_by_waybill(waybill_id: int):
    return select_fields_from_table(
        fields=' * ',
        table=' parcells ',
        where_condition=F' parcells_waybills_id = {waybill_id} ORDER BY parcells_items_id '
    )


def create_parcels_by_api(postman: ua_posts_api.Postman, state_pars: dict):
    """Create parcels using api. First form dicts needed."""

    """  table `contract_waybills` fields:

        SELECT `contract_waybills`.`id_waybills`,
            `contract_waybills`.`delivery_contracts_id`,
            `contract_waybills`.`waybills_receivers_id`,
            `contract_waybills`.`waybills_rps_id`,
            `contract_waybills`.`total_cost`,
            `contract_waybills`.`total_volume`,
            `contract_waybills`.`total_places`,
            `contract_waybills`.`contract_waybills_token`,
            `contract_waybills`.`waybils_pdf_file_name`
        FROM `postman`.`contract_waybills`;

    """

    """  table `receiver_postservice_street` fields:

        SELECT `receiver_postservice_street`.`id_r_p_street`,
            `receiver_postservice_street`.`rps_receivers_id`,
            `receiver_postservice_street`.`rps_postservices_id`,
            `receiver_postservice_street`.`rps_streets_id`
        FROM `postman`.`receiver_postservice_street`;
    """

    """  table `streets` fields:

        SELECT `streets`.`id_streets`,
            `streets`.`city_id`,
            `streets`.`street_name`,
            `streets`.`street_token`
        FROM `postman`.`streets`;
    """

    """  table `parcells` fields:

        SELECT `parcells`.`id_parcells`,
            `parcells`.`parcells_waybills_id`,
            `parcells`.`parcells_items_id`,
            `parcells`.`items_number`,
            `parcells`.`packs_number`,
            `parcells`.`weight_calculated`,
            `parcells`.`height_calculated`,
            `parcells`.`cost_calculated`,
            `parcells`.`parcell_volume_calculated`,
            `parcells`.`pacells_pdf_file`,
            `parcells`.`text_to_sticker`
        FROM `postman`.`parcells`;

    """

    """  table `items` fields:

        SELECT `items`.`id_items`,
            `items`.`delivery_contracts_id`,
            `items`.`item_id_in_delivery`,
            `items`.`item_name`,
            `items`.`item_weight`,
            `items`.`item_cost`,
            `items`.`length`,
            `items`.`width`,
            `items`.`height_x_100`
        FROM `postman`.`items`;
    """

    """    table `receivers` fields:

        SELECT `receivers`.`id_receivers`,
            `receivers`.`id_companies`,
            `receivers`.`surname`,
            `receivers`.`name`,
            `receivers`.`middle_name`,
            `receivers`.`phone`,
            `receivers`.`city`,
            `receivers`.`street`,
            `receivers`.`building`,
            `receivers`.`floor`,
            `receivers`.`flat`,
            `receivers`.`comment`,
            `receivers`.`date_in`,
            `receivers`.`branch`,
            `receivers`.`is_active`,
            `receivers`.`post_ZIP`
        FROM `postman`.`receivers`;
    """

    """  Dictionary for API request example:

                json={
                    "contractID": "a3df71d8-5e17-11ea-80c6-000c29800ae7",
                    "receiverPay": False,
                    # "COD": 600,
                    "notation": ".......",
                    "sender": {
                       "phone": kwargs.get('sender_phone', "+38050-421-1558"),
                       "name": kwargs.get('sender_name', 'Васина Лариса'),
                       },
                    "placesItems": [  # TODO:  form and gives dictionary here &&?
                        {"weight": kwargs['weight'],                        # 1
                         "height": kwargs.get('height', 0.01),              # 2
                         "width":  kwargs.get('width', 0.01),               # 3
                         "length": kwargs.get('length', 0.01),              # 4
                         "insurance": kwargs.get('insurance', 500),
                         "quantity": kwargs.get('quantity', 1),             # 16
                         }
                    ],
                    'contentsItems': [   # TODO:  form and gives dictionary here &&?
                        {
                            'contentName': kwargs['contentName'],           # 6
                            'quantity':	1,
                            'weight': 0.101,                                # 7
                            'value': 0.362,                                 # 8
                        },
                    ],
                    "receiver": {  # TODO:  form and gives dictionary here &&?
                        "name": kwargs['name'],                                # 9
                        "phone": kwargs['phone'],                              # 10
                        "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",
                        "zipCode": kwargs['zipCode'],                          # 11
                        "addressID": kwargs['addreeID'],                       # 12
                        "building": kwargs['building'],                        # 13
                        "flat": kwargs.get('flat', "1"),
                        "floor": kwargs.get('floor', 1),                       #15
                        "service": "Door",
                    },

                    "payType": "noncash",
                }
            )
            self.auth_response_code = response.status_code
            content_result = json.loads(response.content)['result']
            return response.status_code, content_result

    """

    """      def select_fields_from_table(
                fields='id, company_name, short_name_latin',
                table='companies',
                where_condition='is_active'
        ):
    """

    def meest_mult(post_service_id: int, parcells_num: int, packs_num: int):
        if post_service_id == 1:  # MeestExpress
            return 1 if parcells_num == 1 else packs_num
        elif post_service_id == 2:  # NovaPoshta
            return 1
        else:
            ...

    curr_contracts_id = state_pars['delivery_contract']['id_delivery_contract']
    post_service_id = state_pars['post_service']['id_postcervices']

    waybills_for_contract = select_fields_from_table(
        fields='id_waybills, waybills_receivers_id, waybills_rps_id, total_weight ',
        table='contract_waybills',
        where_condition=F'contract_waybills.delivery_contracts_id = {curr_contracts_id}'
    )

    for waybill_row in waybills_for_contract:
        id_waybills, waybills_receivers_id, waybills_rps_id, total_weight = waybill_row

        kwargs = dict(placesItems=[], receiver=None, weight=total_weight)

        parcells_in_waybill = get_ordered_parcells_by_waybill(id_waybills)
        parcells_num = len(parcells_in_waybill)  # !!! fucked MeestExpress formula
        for parcell in parcells_in_waybill:
            (
                id_parcells,
                parcells_waybills_id,   # +
                parcells_items_id,      # +
                items_number,
                packs_number,           # +
                weight_calculated,      # +
                height_calculated,      # +
                cost_calculated,        # +
                parcell_volume_calculated,
                pacells_pdf_file,
                text_to_sticker
            ) = parcell

            item_name, width, length = select_fields_from_table(
                fields=' item_name, width, length ',
                table=' items ',
                where_condition=F' id_items = {parcells_items_id} '
            )[0]

            kwargs["placesItems"].append(
                {
                    "quantity": packs_number,
                    "weight": round(
                        weight_calculated *
                        meest_mult(post_service_id, parcells_num, packs_number), 3),
                    "volume": round(
                        parcell_volume_calculated *
                        meest_mult(post_service_id, parcells_num, packs_number), 3),
                    "insurance": round(
                        cost_calculated *                       # can be ommited
                        meest_mult(post_service_id, parcells_num, packs_number), 2),
                    "length": length,                           # can be ommited
                    "width":  width,                            # can be ommited
                    "height": int(height_calculated),           # can be ommited
                })
            #    sum total w8
            #    find max sizes

        #    Create waybill_row description in 3 steps:
        # Step 1/3. Get postservice street name & address token
        street_name, street_token = select_fields_from_table(  # TODO: CRUD
            fields=' street_name, street_token ',
            table="""receiver_postservice_street t1
             JOIN streets t2
                ON t1.rps_streets_id = t2.id_streets
            """,
            where_condition=F' id_r_p_street = {waybills_rps_id}'
        )[0]
        # Step 2/3. Get point of delivery data:
        (surname, name, middle_name, phone, city, building, floor, flat, post_ZIP
         ) = select_fields_from_table(
            fields=' surname, name, middle_name, phone, city, building, floor, flat, post_ZIP ',
            table=' receivers ',
            where_condition=F' id_receivers = {waybills_receivers_id}'
        )[0]
        # Step 3/3. Form the dict for query:
        kwargs["receiver"] = {
            "name": ' '.join([surname, name, middle_name]),
            "phone": phone,
            "countryID": "c35b6195-4ea3-11de-8591-001d600938f8",

            "addressID": street_token,
            "building": building,
            "service": "Door",
        }

        if post_ZIP:
            kwargs["receiver"]["zipCode"] = post_ZIP
        if floor:
            kwargs["receiver"]["floor"] = int(floor)
        if flat:
            kwargs["receiver"]["flat"] = flat

        print("\n", kwargs)
        #
        #    create parcel with api
        #
        resp_code, result = postman.parcels.create(**kwargs)    # TODO:  split procedure here
        #
        # parcelID
        print(resp_code, result)

        if resp_code == 200 and 'parcelID' in result:
            # TODO: save result['parcelID'] to  table `contract_waybills` field
            update_one(tablename='contract_waybills',
                       fields_name=['contract_waybills_token', 'id_waybills'],
                       values=(result['parcelID'], id_waybills)
                       )


def waybills_sum_filling(delivery_contracts_id: int):

    command = F'''
        SELECT
            ROUND(SUM(cost_calculated * packs_number), 2)  AS total_cost,
            ROUND(SUM(parcell_volume_calculated * packs_number), 2)  AS total_volume,
            ROUND(SUM(weight_calculated * packs_number), 2)  AS total_weight,
            SUM(packs_number) AS total_places,
            parcells_waybills_id
        FROM
            postman.parcells
        WHERE
            parcells_waybills_id IN (SELECT
                    id_waybills
                FROM
                    contract_waybills
                WHERE
                    delivery_contracts_id = {delivery_contracts_id})
        GROUP BY (parcells_waybills_id);
    '''
    cnx = from_server_connect()
    _cursor = cnx.cursor()

    _cursor.execute(command)  # SQL command executing

    selected_data = _cursor.fetchall()
    cnx.commit()
    cnx.close()

    return selected_data


def update_many(tablename: str, fields_name: list, values: list):
    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = "UPDATE {table_n} SET {fields_eq_s}  WHERE {waybils_id}=%s"

    fileds_with_ss = [name+'=%s' for name in fields_name[:-1]]  # last element is ID - do not take

    sql_command = command_pattern.format(
        table_n=tablename,
        fields_eq_s=", ".join(fileds_with_ss),
        waybils_id=fields_name[-1],
    )

    # SQL command executing
    _cursor.executemany(sql_command, values)

    cnx.commit()
    cnx.close()


def update_one(tablename: str, fields_name: list, values: tuple):
    cnx = from_server_connect()
    _cursor = cnx.cursor()   # used inside f-function

    command_pattern = "UPDATE {table_n} SET {fields_eq_s}  WHERE {waybils_id}=%s"

    fileds_with_ss = [name+'=%s' for name in fields_name[:-1]]  # last element is ID - do not take

    sql_command = command_pattern.format(
        table_n=tablename,
        fields_eq_s=", ".join(fileds_with_ss),
        waybils_id=fields_name[-1],
    )

    # SQL command executing
    _cursor.execute(sql_command, values)

    cnx.commit()
    cnx.close()
