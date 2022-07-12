import device
import helpers
import longpolling, auth, time
import opc_ua_client


def main():

    # try login if not wait until do it
    while 1:
        try:
            if not auth.login():
                helpers.wait_connection()
                continue
            # get system info
            device.device_start()
            #start longpolling service
            print('INFO: Starting longpolling...')
            longpolling.poll()
        except:
            helpers.wait_connection()
            print('ERROR: OPC server not found...')



if __name__ == '__main__':
    main()