config = {
    'MACHINE': 'Embalagem 1',

    #SERVER ---------------------------------------------_
    'URL': 'https://erp.nuvensvivazes.com',
    #'URL': 'http://localhost:8069',
    'HEADERS': {'Content-type': 'application/json', "Accept": "application/json"},
    "DB": "nuvens-master-5712383",
    #"DB": "nuv",

    # AUTH ----------------------------------------------
    "LOGIN": "almofadas1_tablet",
    "PASSWORD": "`(4]Py#{.*HT;'(x",
    'AUTH_URL': '/web/session/authenticate',

    #LONGPOLLING ---------------------------------------

    'POLL': '/longpolling/poll',
    'CHANNELS': ['factory'],
    'LONG_IS_ACTIVE': True,
    'LONGPOLLING_LAST': 0,

    #DEVICE ---------------------------------------------
    'DEVICE_URL': '/mrp/opc-ua/vals',
    'SET_DEVICE_URL': '/mrp/opc-ua/set-vals',

    #OPC-UA CLIENT --------------------------------------
    #'OPC_SERVER': "opc.tcp://arxibox:53530/OPCUA/SimulationServer"
    'OPC_SERVER': "opc.tcp://192.168.1.150:4840"
}





