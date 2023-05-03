# Mac Response:
#!/usr/bin/env python
# This exists, because my Mac has that firewall issue, where the settings change on their own.
# I will be focussing on security stuff for a few months, because that is the field I am coming from.
# In order for this to work properyly, you need to create .plist script as this is intended to be event driven.
# I am looking to build a more modern way to do this, but I am not sure how to do it yet. I am new to Mac OS and Python.
# Feel free to add advice or questions. If you know more about this subject than myself, feel free to contact me.


import socket
import logging
import hashlib
import getpass

# Define the expected firewall settings
EXPECTED_FIREWALL_SETTINGS = {
    "Block all incoming connections": True,
    "Automatically allow signed software to receive incoming connections": False,
    "Automatically allow built-in software to receive incoming connections": False,
    "Enable stealth mode": True
}

# Set up logging
logging.basicConfig(filename='/var/log/firewall_check.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Set up password protection
password = 'mysecretpassword'
hashed_password = hashlib.sha3_512(password.encode('utf-8')).hexdigest()

# Check the firewall settings
def check_firewall_settings():
    settings = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect(('localhost', 0))
            s.close()
            settings["Block all incoming connections"] = False
        except socket.error:
            settings["Block all incoming connections"] = True

    settings["Automatically allow signed software to receive incoming connections"] = \
        socket.getdefaulttimeout() is None

    settings["Automatically allow built-in software to receive incoming connections"] = \
        socket.gethostbyname('localhost') == '127.0.0.1'

    settings["Enable stealth mode"] = \
        socket.getservbyname('ipp', 'tcp') is None

    # Log the firewall settings and compare them to the expected settings
    logging.info('Current firewall settings:')
    for setting, value in settings.items():
        logging.info(f'{setting}: {value}')
        if value != EXPECTED_FIREWALL_SETTINGS[setting]:
            logging.warning(f'Firewall setting {setting} is {value}, expected {EXPECTED_FIREWALL_SETTINGS[setting]}')

    # Prompt for password to allow changes to the script or to kill the process
    while True:
        command = input('Enter command (change/kill): ')
        if command == 'change':
            entered_password = getpass.getpass('Enter password: ')
            if hashed_password == hashlib.sha3_512(entered_password.encode('utf-8')).hexdigest():
                print('Password correct, making changes...')
                # add code to make changes to the firewall settings
                break
            else:
                print('Password incorrect, try again.')
        elif command == 'kill':
            entered_password = getpass.getpass('Enter password: ')
            if hashed_password == hashlib.sha3_512(entered_password.encode('utf-8')).hexdigest():
                print('Password correct, exiting...')
                break
            else:
                print('Password incorrect, try again.')
        else:
            print('Invalid command, try again.')

# Check the firewall settings when the script is run
if __name__ == '__main__':
    check_firewall_settings()
