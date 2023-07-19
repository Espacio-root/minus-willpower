from single import MultipleInstances
import sys
import os

def run(time):
    
    website_list_path = 'website_list.txt'
    website_list_path = os.path.join(os.path.dirname(__file__), website_list_path)
    
    MultipleInstances(5, 'website_list.txt', time, 2).block_websites()

if __name__ == '__main__':
    time_to_unblock = float(sys.argv[1])
    run(time_to_unblock)