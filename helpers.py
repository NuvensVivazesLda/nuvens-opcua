from config import config
import json, time
import syslog

time_sleep = 1.0

def request_prepare(message):
    return json.dumps({'jsonrpc': '2.0', 'params': message})

def get_result(message):
    if message.status_code != 200:
        return False
    data = json.loads(message.text)
    if data.get('error'):
        return False
    return data.get('result') if data.get('result') else True


def wait_connection():
    global time_sleep
    syslog.syslog(syslog.LOG_INFO, 'INFO: Retry connection in {} sec'.format(str(time_sleep)))
    time.sleep(time_sleep)
    time_sleep = time_sleep * 2
    if time_sleep > 64:
        reset_time_connection()


def reset_time_connection():
    global time_sleep
    time_sleep = 1.0