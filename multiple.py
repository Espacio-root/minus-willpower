from main import MultipleInstances
import os

if __name__ == '__main__':

    website_list_path = 'website_list.txt'
    website_list_path = os.path.join(os.path.dirname(__file__), website_list_path)
    
    MultipleInstances(10, 'website_list.txt', 60 * 5, 1).block_websites()