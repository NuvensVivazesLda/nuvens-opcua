import device
import helpers
import longpolling, auth, time
import opc_ua_client


import sys
import syslog
import time

def main():

    # try login if not wait until do it

    while 1:
        try:
            if not opc_ua_client.start():
                syslog.syslog(syslog.LOG_INFO, 'ERROR : Connection OPC UA server....')
                helpers.wait_connection()
                continue
            if not auth.login():
                syslog.syslog(syslog.LOG_INFO, 'ERROR : Connecting Odoo server....')
                helpers.wait_connection()
                continue
                # get system info
            device.device_start()
            #start longpolling service
            syslog.syslog(syslog.LOG_INFO, 'INFO : Starting longpolling...')
            longpolling.poll()
        except:
            helpers.wait_connection()
            syslog.syslog(syslog.LOG_INFO, 'ERROR : System start error. Odoo server or OPC server not reacheable...')
            # time.sleep(3)

if __name__ == '__main__':
    main()
