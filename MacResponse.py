# Mac Response
# Trying to fix the pile of crap Mac OS, one script at a time.

# !/usr/bin/env python


import os
import subprocess
import time

# Define the path to the plist file
PLIST_PATH = '/Library/LaunchAgents/com.example.firewall_check.plist'

# Define the command to run when the firewall settings change
COMMAND = ['/usr/bin/logger', '-s', 'Firewall settings have been changed']

# Check the current firewall settings
def check_firewall_settings():
    # Add your firewall settings check code here
    pass

# Run the command when the firewall settings change
def run_command():
    subprocess.run(COMMAND)

# Monitor the firewall settings for changes
def monitor_firewall_settings():
    # Get the modification time of the plist file
    last_modification_time = os.path.getmtime(PLIST_PATH)
    
    # Loop indefinitely, checking the modification time of the plist file
    while True:
        current_modification_time = os.path.getmtime(PLIST_PATH)
        if current_modification_time > last_modification_time:
            # The plist file has been modified, so run the command
            run_command()
            check_firewall_settings()
            # Update the modification time
            last_modification_time = current_modification_time
        
        # Wait for a short period before checking again
        time.sleep(1)

if __name__ == '__main__':
    monitor_firewall_settings()