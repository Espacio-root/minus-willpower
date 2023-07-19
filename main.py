import time
from single import TerminalPreventBlocker, Helper
import sys



if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_list_path = 'website_list.txt'
    delay_between_checks = 2
    arg = sys.argv[1]
    time = min(Helper.handle_time(arg), Helper.handle_time(arg))
    
    instance = TerminalPreventBlocker(website_list_path, time, delay_between_checks)
    [instance.launch_instance() for _ in range(2)]
