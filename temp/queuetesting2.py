import time
from multiprocessing import Process, Queue, Event
import multiprocessing


q = Queue()
stopnow = Event()

def append_to_queue(t=1):
    n = 0
    while not stopnow.is_set():
        q.put(n)
        n += 1
        time.sleep(t)
    q.put("producer done") # consumer will print this

def print_from_queue(t=0.5):
    while not stopnow.is_set():
        print q.get()
        time.sleep(t)
    # drain queue
    for msg in xrange(q.qsize()):
        print msg
    print "consumer done"

def main(t1, t2):
    q = Queue()
    producer = Process(target=append_to_queue, args=(t1,))
    producer.start()
    consumer = Process(target=print_from_queue, args=(t2,))
    consumer.start()
    time.sleep(5)
    stopnow.set()
    producer.join()
    consumer.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main(1, 0.5)