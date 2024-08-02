import datetime

import device
import opc_ua_client
from config import config
import json, requests, helpers, time
import syslog

longpoll_last = config['LONGPOLLING_LAST']

def get_poll_url():
    return config['URL'] + config['POLL']

def get_longpolling_params():
    param = {
        'channels': config['CHANNELS'],
        'last': longpoll_last,
        'options': {'shadow': True}
    }
    return helpers.request_prepare(param)


def on_poll(notification):
    global longpoll_last

    vals = helpers.get_result(notification)
    if not vals:
        return

    if type(vals) != bool: #TODO I DON 'T LIKED...
        values_to_send = []
        #print('INFO: New pool message received : ', vals)
        for rec in vals:
            if rec.get('id') > longpoll_last:
                longpoll_last = rec.get('id')
                syslog.syslog(syslog.LOG_INFO, 'INFO : longpolling last message: [ {} ]'.format(longpoll_last))
                if rec.get('message').get('payload').get('from') in device.device['listening_devices']:
                    if rec.get('message').get('payload').get('action') == 'data':
                        for item in rec.get('message').get('payload').get('payload'):
                            #syslog.syslog(syslog.LOG_INFO, 'item', item)
                            value = None
                            if item.get('read'):
                                value = opc_ua_client.read_value(item.get('namespace'), item.get('identifier'), item.get('variable_type'))
                                values_to_send.append(value)
                            elif item.get('write'):
                                value = opc_ua_client.write_value(item.get('namespace'), item.get('identifier'), item.get('variable_type'), item.get('value'))
                                values_to_send.append(value)
                            if not value:
                                return False
                        # syslog.syslog(syslog.LOG_INFO, 'INFO: {} : Updating device data...'.format(datetime.datetime.now()))
                        # device.device_start()
                    elif rec.get('message').get('payload').get('action') == 'refresh':
                        device.device_start()
                        return rec['message']['payload']

                # return rec['message']['payload']
        device.set_device_values(values_to_send)
    return True


def poll():
    longpolling_is_active= config['LONG_IS_ACTIVE']
    syslog.syslog(syslog.LOG_INFO, 'INFO : New pool connection started...')
    try:
        long_result = requests.post(get_poll_url(), data=get_longpolling_params(), timeout=60000,
                                    headers=config['HEADERS'])
        if not on_poll(long_result):
            longpolling_is_active = False
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, 'ERROR : Error while processing _onPoll registering a new _poll request')
    finally:
        syslog.syslog(syslog.LOG_INFO, 'INFO : New pool connection ended...')
        if longpolling_is_active:
            poll()

