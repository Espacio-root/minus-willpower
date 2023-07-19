import time
from single import TerminalPreventBlocker, Helper
import sys



if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_list_path = 'website_list.txt'
    delay_between_checks = 2
    arg = sys.argv[1]
    arg = Helper.handle_time(arg)
    arg = min(arg, max_time_period)
    
    instance = TerminalPreventBlocker(website_list_path, arg, delay_between_checks)
    [instance.launch_instance() for _ in range(2)]
