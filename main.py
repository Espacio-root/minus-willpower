from time import sleep, time
from single import TerminalPreventBlocker, Helper
import sys



if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_list_path = 'websites.txt'
    delay_between_checks = 2
    arg = sys.argv[1]
    time = int(arg) if int(arg) > time() and int(arg) < time() + max_time_period else min(Helper.handle_time(arg), Helper.handle_time(max_time_period))
    
    instance = TerminalPreventBlocker(website_list_path, time, delay_between_checks * 2)
    
    with open(r"C:\Users\Rizwan\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\asdjfasdfjads.bat", 'w') as fp:
        fp.write(f'@echo off\npythonw "C:\\Projects\\minus-willpower\\main.py" {time}')

    for _ in range(2):
        instance.launch_instance(delay_between_checks)
        sleep(delay_between_checks)
