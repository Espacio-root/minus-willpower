from time import sleep, time
from single import TerminalPreventBlocker, Helper
import sys
import os

if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_list_path = 'websites.txt'
    delay_between_checks = 2
    arg = sys.argv[1]
    time = int(arg) if int(arg) > time() and int(arg) < time() + max_time_period else min(Helper.handle_time(arg), Helper.handle_time(max_time_period))
    
    instance = TerminalPreventBlocker(website_list_path, time, delay_between_checks * 2)
    
    # get c dir
    user_dir = os.path.join(os.path.expanduser('~'), r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup", 'minus-willpower.bat')
    cur_dir = os.path.join(os.path.dirname(__file__), 'main.py')
    content = f'@echo off\npythonw "{cur_dir}" {time}'

    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    with open(user_dir, 'w') as fp:
        fp.write(content)

    for _ in range(2):
        instance.launch_instance(delay_between_checks)
        sleep(delay_between_checks)
        
    while True:
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        with open(user_dir, 'r') as fp:
            new_content = fp.read()
        
        if new_content != content:
            with open(user_dir, 'w') as fp:
                fp.write(content)
                
