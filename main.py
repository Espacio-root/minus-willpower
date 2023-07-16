import platform
from time import time, sleep
import re
import sys
import os
import subprocess
import psutil

class WebsiteBlocker:
    
    def __init__(self, website_list_path):
        self.hosts_path = self._initialize_host_path()
        self.website_list_path = website_list_path
        self._initial_website_list = self.website_list
        
    @property
    def hosts_content(self):
        with open(self.hosts_path, 'r') as fp:
            return fp.read()
    
    @property
    def website_list(self):
        with open(self.website_list_path, 'r') as fp:
            return fp.read().split('\n')
        
    def _initialize_host_path(self):
        system = platform.system()

        if system == 'Windows':
            return r'C:\Windows\System32\drivers\etc\hosts'
        elif system == 'Linux' or system == 'Darwin':
            return '/etc/hosts'
        else:
            raise Exception('OS currently not supported')

    def update_host_file(self):
        with open(self.hosts_path, 'a') as host_file:
            content = self.hosts_content
            pattern = r'^127\.0\.0\.1\s+\S+'
            matches = re.findall(pattern, content, re.MULTILINE)
            modified_content = ''.join(matches)
            res = []
            
            for website in self._initial_website_list:
                if website in modified_content:
                    continue
                res.append(website)
                host_file.write(f'127.0.0.1 {website}\n')

            return res

class ConstantWebsiteBlocker(WebsiteBlocker):
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks):
        super().__init__(website_list_path)
        
        self.time_to_unblock = time_to_unblock
        self.delay = delay_between_checks
        
    def block_websites(self):
        while time() <= self.time_to_unblock:
            self.update_host_file()
            sleep(self.delay)
            
class MultipleInstances:
    def __init__(self, num_processes, website_list_path, time_to_unblock, delay_between_checks):
        
        self.num_processes = num_processes
        self.check_delay = delay_between_checks * num_processes
        self.website_list_path = website_list_path
        self.delay = delay_between_checks

        time_buffer = min(time_to_unblock, 24 * 60 * 60)
        self.time_to_unblock = time() + time_buffer
        
    @staticmethod
    def launch_pythonw(command, *args):
        args = [str(arg) for arg in args]
        args = ' '.join(args)
        subprocess.Popen(['python', command, args])

    def launch_instances(self, num):
        for _ in range(num):
            file_path = os.path.join(os.path.dirname(__file__), 'main.py')
            MultipleInstances.launch_pythonw(file_path, self.website_list_path, self.time_to_unblock, self.delay)
            sleep(self.delay)
            
            
    def track_instances(self):
        def count_pythonw_instances(name):
            count = 0
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == name:
                    count += 1
            return count
        initial_num_instances = count_pythonw_instances('python.exe')

        while time() <= self.time_to_unblock:
            num_instances = count_pythonw_instances('python.exe')
            if num_instances < initial_num_instances:
                self.launch_pythonw(os.path.join(os.path.dirname(__file__), 'multiple.py'))
                sleep(self.delay)
                
    def block_websites(self):
        self.launch_instances(self.num_processes)
        self.track_instances()
            
if __name__ == '__main__':
    
    args = sys.argv[1:]
    args = args[0].split(' ')

    blocker = ConstantWebsiteBlocker(args[0], float(args[1]), int(args[2]))
    blocker.block_websites()
            