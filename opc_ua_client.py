import datetime
import time

import device
import helpers
from config import config
from opcua import Client, ua
import syslog

client = Client(url=config['OPC_SERVER'])

node_list = []
opc_connected = False

def start():
    try:
        if not get_status():
            return False
        syslog.syslog(syslog.LOG_INFO, '------------------------------------------------------')
        syslog.syslog(syslog.LOG_INFO, 'OPC-UA SERVER [OK]')
        syslog.syslog(syslog.LOG_INFO, 'SERVER URL: {}'.format(config['OPC_SERVER']))
        return True
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)
        return False

def connect():
    global opc_connected
    try:
        client.connect()
        #syslog.syslog(syslog.LOG_INFO, 'INFO : connecting socket opc service...')
        opc_connected = True
        return True
    except:
        syslog.syslog(syslog.LOG_INFO, 'ERROR: Try connect opc again')
        time.sleep(1)
        connect()

def disconnect():
    try:
        client.disconnect()
        #syslog.syslog(syslog.LOG_INFO, 'INFO : disconnecting socket opc service...')
        opc_connected = False
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)


def get_status():
    try:
        connect()
        root = client.get_root_node()
        return root if root else False
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)
        return False
    finally:
        disconnect()

def delete_node_list():
    global node_list
    node_list = []

def check_type(type):
    if type and type == 'str':
        return 's'
    else:
        return 'i'

def update_values():
    syslog.syslog(syslog.LOG_INFO, 'INFO : OPC-ua, update values')
    if not get_status():
        return False
    delete_node_list()
    try:
        connect()
        for node in device.device['data']:
            if node.get('namespace') and node.get('identifier'):
                #syslog.syslog(syslog.LOG_INFO, "ns={};{}={}".format(node.get('namespace'), check_type(node.get('variable_type')), node.get('identifier')))
                nd = client.get_node("ns={};{}={}".format(node.get('namespace'), check_type(node.get('variable_type')), node.get('identifier')))
                if nd.get_type_definition():
                    node_list.append({
                        'type':       'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                        'name':       nd.get_display_name().Text,
                        'namespace':  nd.nodeid.NamespaceIndex,
                        'identifier': nd.nodeid.Identifier,
                        #'parent':     nd.get_parent().get_display_name().Text,
                        'value':      nd.get_value()
                    })
                else:
                    node_list.append({
                        'type':       None,
                        'name':       'NODE NOT FOUND...',
                        'namespace':  node.get('namespace'),
                        'identifier': node.get('identifier'),
                        'parent':     None,
                        'value':      None,
                    })
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)
        #client.disconnect()
        return False
    finally:
        disconnect()

def read_value(namespace, identifier, type):
    syslog.syslog(syslog.LOG_INFO, 'INFO : {} : OPC-ua, read values'.format(datetime.datetime.now()))
    if not get_status():
        return False
    try:
        connect()
        nd = client.get_node("ns={};{}={}".format(namespace, check_type(type), identifier))
        if nd.get_type_definition():
            return {
                'type': 'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                'name': nd.get_display_name().Text,
                'namespace': nd.nodeid.NamespaceIndex,
                'identifier'
                ''
                '': nd.nodeid.Identifier,
                'parent': nd.get_parent().get_display_name().Text,
                'value': nd.get_value(),
            }
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)
        return False
    finally:
        disconnect()


def write_value(namespace, identifier, type, value):
    syslog.syslog(syslog.LOG_INFO, 'INFO : {} : OPC-ua, write values'.format(datetime.datetime.now()))
    if not get_status():
        return False
    connect()
    try:
        nd = client.get_node("ns={};{}={}".format(namespace, check_type(type), identifier))
        if nd.get_type_definition():
            variant_type = nd.get_data_type_as_variant_type()
            if variant_type == ua.VariantType.Boolean:
                value = ua.DataValue(ua.Variant(False if value == 'False' or value == '0' or value == 0 else True, ua.VariantType.Boolean))
                nd.set_value(value)
            elif variant_type == ua.VariantType.String:
                value = ua.DataValue(ua.Variant(value, ua.VariantType.String))
                a = nd.set_value(value)
            elif variant_type in (ua.VariantType.Float, ua.VariantType.Double):
                nd.set_value(float(value))
            elif variant_type in (ua.VariantType.Int32, ua.VariantType.Int16, ua.VariantType.Int64):
                nd.set_value(int(value))
            return {
                'type': 'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                'name': nd.get_display_name().Text,
                'namespace': nd.nodeid.NamespaceIndex,
                'identifier': nd.nodeid.Identifier,
                #'parent': nd.get_parent().get_display_name().Text,
                'value': nd.get_value(),
            }
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, e)
        return False
    finally:
        disconnect()