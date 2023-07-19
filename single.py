import platform
from time import time, sleep
import re
import sys
import os
import subprocess
import psutil
from threading import Thread

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
        hosts_content = self.hosts_content
        # pattern = r'^127\.0\.0\.1\s+\S+'
        # matches = re.findall(pattern, content, re.MULTILINE)
        website_list_content = [f'127.0.0.1 {website}\n' for website in self._initial_website_list if website.strip() != '']
        website_list_content = ''.join(website_list_content)
            
        if hosts_content != website_list_content:
            with open(self.hosts_path, 'w') as host_file:
                host_file.write(website_list_content)


class ConstantWebsiteBlocker(WebsiteBlocker):
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks):
        super().__init__(website_list_path)
        
        self.time_to_unblock = float(time_to_unblock)
        self.delay = int(delay_between_checks)
        
    def block_websites(self):
        while time() <= self.time_to_unblock:
            self.update_host_file()
            sleep(self.delay)
            
class TerminalPreventBlocker(ConstantWebsiteBlocker):
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks):
        super().__init__(website_list_path, time_to_unblock, delay_between_checks)

        self.launch_instance = lambda: subprocess.Popen(['python', os.path.join(os.path.dirname(__file__), 'single.py'), str(self.website_list_path), str(self.time_to_unblock), str(self.delay)])
    
    def track_instances(self):
        def pythonw_instances():
            instances = []
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] == 'python.exe':  # type: ignore
                    instances.append(proc.info['pid']) # type: ignore
            return instances
        prev_instances = pythonw_instances()
        
        while time() <= self.time_to_unblock:
            cur_instances = pythonw_instances()
            if len(cur_instances) < len(prev_instances):
                self.launch_instance()
            prev_instances = cur_instances
    
    def block_websites(self):
        tracker = Thread(target=self.track_instances)
        tracker.start()
        super().block_websites()
        
class Helper:
    
    @staticmethod
    def handle_time(cur_time: str or int or float) -> float:
        if isinstance(cur_time, str):
            if ':' not in cur_time:
                return float(cur_time)
            
            li = cur_time.split(':')
            li.reverse()
            li = [li[i] + '*60' * i for i in range(len(li))]
            cur_time = '+'.join(li)
            

            cur_time = eval(cur_time)
        
        return float(cur_time) + time()
    
            
# class MultipleInstances:
#     def __init__(self, num_processes, website_list_path, time_to_unblock, delay_between_checks):
        
#         self.num_processes = num_processes
#         self.check_delay = delay_between_checks * num_processes
#         self.website_list_path = website_list_path
#         self.delay = delay_between_checks
#         self.time_to_unblock = time_to_unblock

        
#     @staticmethod
#     def launch_pythonw(command, *args):
#         args = [str(arg) for arg in args]
#         args = ' '.join(args)
#         subprocess.Popen(['pythonw', command, args])

#     def launch_instances(self, num):
#         for _ in range(num):
#             file_path = os.path.join(os.path.dirname(__file__), 'single.py')
#             MultipleInstances.launch_pythonw(file_path, self.website_list_path, self.time_to_unblock, self.delay)
#             sleep(self.delay)
            
            
#     def track_instances(self):
#         def count_pythonw_instances(name):
#             count = 0
#             for proc in psutil.process_iter(['name']):
#                 if proc.info['name'] == name:  # type: ignore
#                     count += 1
#             return count
#         initial_num_instances = count_pythonw_instances('pythonw.exe')

#         while time() <= self.time_to_unblock:
#             num_instances = count_pythonw_instances('pythonw.exe')
#             if num_instances < initial_num_instances:
#                 self.launch_pythonw(os.path.join(os.path.dirname(__file__), 'multiple.py'), self.time_to_unblock)
#                 break
                
#     def block_websites(self):
#         self.launch_instances(self.num_processes)
#         self.track_instances()
            
if __name__ == '__main__':
    
    args = sys.argv[1:]

    # website_list_path, time_to_unblock, delay_between_checks
    blocker = TerminalPreventBlocker(args[0], args[1], args[2])
    blocker.block_websites()
            