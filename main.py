from multiple import run
import time

if __name__ == '__main__':
    time_buffer = 60
    time_to_unblock = time.time() + time_buffer
    
    run(time_to_unblock)