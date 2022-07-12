import helpers
import opc_ua_client
from config import config
import requests, auth


device = {}

def set_device_url():
    return config['URL'] + config['SET_DEVICE_URL']

def get_device_url():
    return config['URL'] + config['DEVICE_URL']

def get_cookies():
    return {'session_id': auth.user['session_id']}

def set_device_info():
    requests.post(set_device_url(), data=helpers.request_prepare({'data': opc_ua_client.node_list}), timeout=60000, headers=config['HEADERS'], cookies=get_cookies())

def get_device_info():
    global device
    device_info = requests.get(get_device_url(), data=helpers.request_prepare({}), timeout=60000, headers=config['HEADERS'], cookies=get_cookies())
    device = helpers.get_result(device_info)

def device_start():
    get_device_info()
    if opc_ua_client.get_status():
        opc_ua_client.update_values()
        set_device_info()
    # set_device_info()

def set_device_values(list):
    requests.post(set_device_url(), data=helpers.request_prepare({'data': list}), timeout=60000, headers=config['HEADERS'], cookies=get_cookies())
