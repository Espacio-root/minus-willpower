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
    cur_dir = os.path.join(os.path.expanduser('~'), r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup", 'minus-willpower.bat')
    content = f'@echo off\npythonw "C:\\Projects\\minus-willpower\\main.py" {time}'

    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
        
    with open(cur_dir, 'w') as fp:
        fp.write(content)

    for _ in range(2):
        instance.launch_instance(delay_between_checks)
        sleep(delay_between_checks)
        
    while True:
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)

        with open(cur_dir, 'r') as fp:
            new_content = fp.read()
        
        if new_content != content:
            with open(cur_dir, 'w') as fp:
                fp.write(content)
                
