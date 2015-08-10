import time
from multiprocessing import Process, Queue, Event
import multiprocessing

def append_to_queue(q, t=1):
    n = 0
    while True:
        q.put(n)
        n += 1
        time.sleep(t)

def print_queue(q, t=0.5):
    while True:
        print q.get()
        time.sleep(t)

def main(t1, t2, delay=1):
    q = Queue()
    p = Process(target=append_to_queue, args=(q, t1,))
    p.start()
    time.sleep(delay)
    print_queue(q, t2)
    p.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main(0.01, 0.1, delay=1)