
import requests
import helpers
from config import config
import syslog

user = {
    'uid': 0,
    'name': None,
    'session_id': None
}

def get_auth_url():
    return config['URL'] + config['AUTH_URL']

data = {
    "login": config['LOGIN'],
    "password": config['PASSWORD'],
    "db": config['DB']
}

def login():
    global user
    req = requests.post(get_auth_url(), data=helpers.request_prepare(data), headers=config['HEADERS'])
    user_data = helpers.get_result(req)
    if not user_data:
        return False
    if user_data.get('uid'):
        user['uid'] = user_data.get('uid')
        user['name'] = user_data.get('name')
        user['session_id'] = req.cookies["session_id"]

        syslog.syslog(syslog.LOG_INFO, '------------------------------------------------------')
        syslog.syslog(syslog.LOG_INFO, 'LOGIN [OK]')
        syslog.syslog(syslog.LOG_INFO, 'id: {}'.format(user['uid']))
        syslog.syslog(syslog.LOG_INFO, 'name: {}'.format(user['name']))
        syslog.syslog(syslog.LOG_INFO, 'session_id: {}'.format(user['session_id']))
        syslog.syslog(syslog.LOG_INFO, '------------------------------------------------------')
        #helpers.reset_time_connection()
        return True
    else:
        return False
#
#
