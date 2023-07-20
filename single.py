import platform
from time import time, sleep
import sys
import os
import subprocess
import psutil
from threading import Thread

class WebsiteBlocker:
    
    def __init__(self, website_list_path):
        self.hosts_path = self._initialize_host_path()
        self.website_list_path = website_list_path

        initial_website_list = self.website_list
        self.website_list_content = lambda website_list: [f'127.0.0.1 {website}\n' for website in website_list if website.strip() != '' and '#' not in website]
        self.initial_website_content = ''.join(self.website_list_content(initial_website_list))
        
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

    def block_websites(self):
        hosts_content = self.hosts_content
        # pattern = r'^127\.0\.0\.1\s+\S+'
        # matches = re.findall(pattern, content, re.MULTILINE)
        cur_website_list = self.website_list_content(self.website_list)
        updated_list = [website for website in cur_website_list if website not in self.initial_website_content]
        self.initial_website_content += ''.join(updated_list)
            
        if hosts_content != self.initial_website_content:
            with open(self.hosts_path, 'w') as host_file:
                host_file.write(self.initial_website_content)


class ConstantWebsiteBlocker(WebsiteBlocker):
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks):
        super().__init__(website_list_path)
        
        self.time_to_unblock = float(time_to_unblock)
        self.delay = int(delay_between_checks)
        
    def block_websites(self):
        while time() <= self.time_to_unblock:
            super().block_websites()
            sleep(self.delay)
            
class TerminalPreventBlocker(ConstantWebsiteBlocker):
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks, track_delay=0):
        super().__init__(website_list_path, time_to_unblock, delay_between_checks)

        self.track_delay = track_delay
        self.launch_instance = lambda x: subprocess.Popen(['pythonw', os.path.join(os.path.dirname(__file__), 'single.py'), str(self.website_list_path), str(self.time_to_unblock), str(self.delay), str(x)])
    
    def track_instances(self):
        def pythonw_instances():
            instances = []
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] == 'pythonw.exe':  # type: ignore
                    instances.append(proc.info['pid']) # type: ignore
            return instances
        
        initial_time = time()
        while time() - initial_time <= self.track_delay * 2:
            continue
        prev_instances = pythonw_instances()
        
        while time() <= self.time_to_unblock:
            cur_instances = pythonw_instances()
            for instance in prev_instances:
                if instance not in cur_instances:
                    self.launch_instance(0)
                    prev_instances = cur_instances
    
    def block_websites(self):
        tracker = Thread(target=self.track_instances)
        tracker.start()
        super().block_websites()
        
class Helper:
    
    @staticmethod
    def handle_time(cur_time: str | int | float) -> float:
        if isinstance(cur_time, str):
            if ':' not in cur_time:
                return float(cur_time)
            
            li = cur_time.split(':')
            li.reverse()
            li = [li[i] + '*60' * i for i in range(len(li))]
            cur_time = '+'.join(li)
            

            cur_time = eval(cur_time)
        
        return float(cur_time) + time()
            
if __name__ == '__main__':
    
    args = sys.argv[1:]

    # website_list_path, time_to_unblock, delay_between_checks
    blocker = TerminalPreventBlocker(args[0], args[1], args[2], int(args[3]))
    blocker.block_websites()
            