from time import sleep, time
from single import TerminalPreventBlocker, Helper
import sys
import os

if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_file_name = 'websites.txt'
    website_list_path = os.path.join(os.path.dirname(__file__), website_file_name)
    delay_between_checks = 2
    arg = sys.argv[1]
    try:
        time = float(arg) if float(arg) > time() and float(arg) < time() + max_time_period else 0
    except:
        time = min(Helper.handle_time(arg), Helper.handle_time(max_time_period))
    
    instance = TerminalPreventBlocker(website_list_path, time, delay_between_checks * 2)
    
    for _ in range(2):
        instance.launch_instance(delay_between_checks)
        sleep(delay_between_checks)
        