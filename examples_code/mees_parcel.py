mees_parcel = {
  {
    'parcelNumber':	'%%%%',  # optional	TST-2550636	Shipment number
    'notation':	'%%%%',      # optional	notation	Notation, comment
    'payType':  'noncash',   # required	cash	Payment type. Options: cash, noncash
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
              'service':	'Door'  # -  required	Branch	Delivery type. Options: Door, Branch
      },  # -  object	required

    #  %%%% 'placesItems'  -  ширина/длина/высота/ название объекта  -  или описание/комментарий
    # %%%%%%  -  placesItems	array	required  Places Items [array] with {object}s block
    'contentsItems': [
        {  # -  Places Items {object} block start
            # %%%% -  string	required	trouses	Content name            %%%%
            'contentName': "Поліграфія",
            'serialNumber': "",  # %%%%  string	optional	SN34943516546546	Serial Number % % % %
            'quantity':	1,  # required	1	Places quantity
            'weight': -1,  # number($float)      # - 	required	0.589	Weight, kg. Type: float(8,3)
            'volume': -3.62,  # number($float)  optional	5.121	Volume. Type: float(7, 3)
            # number   ($float)	optional	200	Declared value of shipping. Type: float(9, 2)
            'insurance': -100,
            # %%%%   optional	c26956ba-a2ce-11e4-b90b-003048d2b473	Unique pack ID.
            #         Obtained by “packTypes” function
            'packID':	'',
            # %%%%%%%%%%%% integer($int32) - -- -- -- -  optional	20	Length, cm
            'length': -20,
            'width': -20,  # %%%% integer($int32), optional	30	Width, cm
            'height': -20,	  # optional	integer($int32),10	Height, cm
        },
      ]
}
