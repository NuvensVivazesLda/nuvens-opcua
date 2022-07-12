
import requests
import helpers
from config import config

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

        print('------------------------------------------------------')
        print('LOGIN [OK]')
        print('id: {}'.format(user['uid']))
        print('name: {}'.format(user['name']))
        print('session_id: {}'.format(user['session_id']))
        print('------------------------------------------------------')
        helpers.reset_time_connection()
        return True
    else:
        return False
#
#