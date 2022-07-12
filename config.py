config = {
    'MACHINE': 'Embalagem',

    #SERVER ---------------------------------------------_
    # 'URL': 'https://nuvens-staging-5143782.dev.odoo.com',
    'URL': 'http://localhost:8069',
    'HEADERS': {'Content-type': 'application/json', "Accept": "application/json"},
    # "DB": "nuvens-staging-5143782",
    "DB": "nuvens",

    # AUTH ----------------------------------------------
    "LOGIN": "embalagens1_tablet",
    "PASSWORD": "embalagens1_tablet",
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
    # 'OPC_SERVER': "opc.tcp://arxibox:53530/OPCUA/SimulationServer"
    'OPC_SERVER': "opc.tcp://miguel-Lenovo-Y520-15IKBN:53530/OPCUA/SimulationServer"
    # 'OPC_SERVER': "opc.tcp://192.168.1.150:4840"
}





