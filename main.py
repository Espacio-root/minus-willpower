from time import sleep
from single import TerminalPreventBlocker, Helper
import sys



if __name__ == '__main__':

    max_time_period = 24 * 60 * 60

    website_list_path = 'website_list.txt'
    delay_between_checks = 2
    arg = sys.argv[1]
    time = min(Helper.handle_time(arg), Helper.handle_time(arg))
    
    instance = TerminalPreventBlocker(website_list_path, time, delay_between_checks * 2)

    for _ in range(2):
        instance.launch_instance(delay_between_checks)
        sleep(delay_between_checks)
