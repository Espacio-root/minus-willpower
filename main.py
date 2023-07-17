import time
from multiple import run
import sys


def handle_time(time: str or int or float) -> float:
    if isinstance(time, int):
        return float(time)
    elif isinstance(time, float):
        return time
    elif isinstance(time, str):
        if ':' not in time:
            return float(time)
        
        li = time.split(':')
        li.reverse()
        li = [li[i] + '*60' * i for i in range(len(li))]
        time = '+'.join(li)

        return float(eval(time))

if __name__ == '__main__':
    time_buffer = str(sys.argv[1])
    time_buffer = handle_time(time_buffer)

    time_to_unblock = time.time() + time_buffer

    run(time_to_unblock)
