import platform
from time import time, sleep
import sys
import os
import subprocess
import psutil
from threading import Thread
from datetime import datetime, timedelta


class WebsiteBlocker:

    def __init__(self, website_list_path):
        
        user_path = os.path.expanduser('~')
        self.python_cmd = 'pythonw'
        self.python_executable = os.path.join(user_path, 'AppData', 'Local', 'Programs', 'Python', 'Python311', f'{self.python_cmd}.exe')
        self.hosts_path = self._initialize_host_path()
        self.website_list_path = website_list_path

        initial_website_list = self.website_list
        self.website_list_content = lambda website_list: [
            f'127.0.0.1 {website}\n' for website in website_list if website.strip() != '' and '#' not in website]
        self.initial_website_content = ''.join(
            self.website_list_content(initial_website_list))

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
        updated_list = [
            website for website in cur_website_list if website not in self.initial_website_content]
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
        self.launch_instance = lambda x: subprocess.Popen([self.python_cmd, os.path.join(os.path.dirname(
            __file__), 'single.py'), str(self.website_list_path), str(self.time_to_unblock), str(self.delay), str(x)])
        self.cur_script_path = os.path.join(
            os.path.dirname(__file__), 'single.py')
        self.initial_script_content = self.get_script_content()

    def get_script_content(self):
        if not os.path.exists(self.cur_script_path):
            os.makedirs(self.cur_script_path)
            return ''

        with open(self.cur_script_path, 'r') as fp:
            return fp.read()

    def verify_script_integrity(self):
        cur_file_content = self.get_script_content()
        if cur_file_content != self.initial_script_content:
            with open(self.cur_script_path, 'w') as fp:
                fp.write(self.initial_script_content)


    def track_instances(self):
        def get_instances(name):
            instances = []
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] == name:  # type: ignore
                    instances.append(proc.info['pid'])  # type: ignore
            return instances

        def verify_task_manger():
            instances = get_instances('Taskmgr.exe')
            if len(instances) > 0:
                for pid in instances:
                    try:
                        os.kill(pid, 9)
                    except:
                        pass

        initial_time = time()
        while time() - initial_time <= self.track_delay * 2:
            continue
        prev_instances = get_instances(f'{self.python_cmd}.exe')

        while time() <= self.time_to_unblock:
            cur_instances = get_instances(f'{self.python_cmd}.exe')
            verify_task_manger()
            
            for instance in prev_instances:
                if instance not in cur_instances:
                    self.verify_script_integrity()
                    self.launch_instance(0)
                    prev_instances = cur_instances

    def block_websites(self):
        tracker = Thread(target=self.track_instances)
        tracker.start()
        super().block_websites()
        
class RestartPreventBlocker(TerminalPreventBlocker):
    
    def __init__(self, website_list_path, time_to_unblock, delay_between_checks, track_delay=0):
        super().__init__(website_list_path, time_to_unblock, delay_between_checks, track_delay)

        self.task_name = "MinusWillpower"
     
    def create_task(self):
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        
        task_command = [
            "schtasks",
            "/create",
            "/tn",
            self.task_name,
            "/tr",
            f"{self.python_executable} \"{script_path}\" \"{self.time_to_unblock}\"",
            "/sc",
            "ONLOGON", # Run on logon
            "/RU",
            "EVERYONE", # Run as the current user
            "/RL",
            "HIGHEST",  # Run with highest privileges
        ]

        try:
            subprocess.run(task_command, check=True, shell=True)
        except subprocess.CalledProcessError:
            pass
    
    def delete_task(self, task_name):
        try:
            task_delete = f"schtasks /delete /tn {task_name} /f"
            subprocess.run(task_delete, check=True)
        except subprocess.CalledProcessError:
            pass
            
    def is_task_running(self, task_name):
        try:
            task_query = f"schtasks /query /tn {task_name}"
            task_output = subprocess.run(task_query, check=True, capture_output=True, text=True, stderr=subprocess.PIPE)
            return "Ready" in task_output.stdout
        except subprocess.CalledProcessError:
            return False

    def track_scheduler(self):
        initial_time = time()
        while time() - initial_time <= self.track_delay * 2:
            continue
        
        if self.is_task_running(self.task_name):
            self.delete_task(self.task_name)
        while time() <= float(self.time_to_unblock):
            cur_task = self.is_task_running(self.task_name)
            if cur_task == False:
                self.create_task()
                
    def block_websites(self):
        scheduler_thread = Thread(target=self.track_scheduler)
        scheduler_thread.start()
        
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
    blocker = RestartPreventBlocker(args[0], args[1], args[2], int(args[3]))
    blocker.block_websites()
