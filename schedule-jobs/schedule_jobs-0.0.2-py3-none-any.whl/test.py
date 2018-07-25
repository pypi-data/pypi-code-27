import time
import threading
import schedule
from queue import Queue
import gevent
from multiprocessing import Process,Queue as PQueue

def job(num, txt: str = "I'm working"):
    def func():
        time.sleep(1)
        print(txt, num)

    return func


def worker_main():
    while 1:
        job_func = jobqueue.get()
        job_func()
        jobqueue.task_done()


def worker_main2():
    while 1:
        job_func = jobqueue2.get()
        job_func()
        jobqueue2.task_done()


def worker_main3():
    while 1:
        job_func = jobqueue3.get()
        job_func()
        jobqueue3.task_done()


def worker_main4():
    while 1:
        job_func = jobqueue4.get()
        job_func()
        jobqueue4.task_done()


def worker_main5():
    while 1:
        job_func = jobqueue5.get()
        job_func()
        jobqueue5.task_done()


jobqueue = Queue(maxsize=2)
jobqueue2 = Queue(maxsize=2)
jobqueue3 = Queue(maxsize=2)
jobqueue4 = Queue(maxsize=2)
jobqueue5 = Queue(maxsize=2)

schedule.every(10).seconds.do(jobqueue.put, job(1))
schedule.every(10).seconds.do(jobqueue.put, job(2))
schedule.every(10).seconds.do(jobqueue.put, job(3))
schedule.every(10).seconds.do(jobqueue.put, job(4))
schedule.every(10).seconds.do(jobqueue.put, job(5))

schedule.every(10).seconds.do(jobqueue2.put, job(1, 'b'))
schedule.every(10).seconds.do(jobqueue2.put, job(2, 'b'))
schedule.every(10).seconds.do(jobqueue2.put, job(3, 'b'))
schedule.every(10).seconds.do(jobqueue2.put, job(4, 'b'))
schedule.every(10).seconds.do(jobqueue2.put, job(5, 'b'))

schedule.every(10).seconds.do(jobqueue3.put, job(1, 'c'))
schedule.every(10).seconds.do(jobqueue3.put, job(2, 'c'))
schedule.every(10).seconds.do(jobqueue3.put, job(3, 'c'))
schedule.every(10).seconds.do(jobqueue3.put, job(4, 'c'))
schedule.every(10).seconds.do(jobqueue3.put, job(5, 'c'))

schedule.every(10).seconds.do(jobqueue4.put, job(1, 'd'))
schedule.every(10).seconds.do(jobqueue4.put, job(2, 'd'))
schedule.every(10).seconds.do(jobqueue4.put, job(3, 'd'))
schedule.every(10).seconds.do(jobqueue4.put, job(4, 'd'))
schedule.every(10).seconds.do(jobqueue4.put, job(5, 'd'))

schedule.every(10).seconds.do(jobqueue5.put, job(1, 'e'))
schedule.every(10).seconds.do(jobqueue5.put, job(2, 'e'))
schedule.every(10).seconds.do(jobqueue5.put, job(3, 'e'))
schedule.every(10).seconds.do(jobqueue5.put, job(4, 'e'))
schedule.every(10).seconds.do(jobqueue5.put, job(5, 'e'))

worker_thread = threading.Thread(target=worker_main, daemon=True)
worker_thread.start()
worker_thread2 = threading.Thread(target=worker_main2, daemon=True)
worker_thread2.start()
worker_thread3 = threading.Thread(target=worker_main3, daemon=True)
worker_thread3.start()
worker_thread4 = threading.Thread(target=worker_main4, daemon=True)
worker_thread4.start()
worker_thread5 = threading.Thread(target=worker_main, daemon=True)
worker_thread5.start()

# g_list = []
# g_list.append(gevent.spawn(worker_main))
# g_list.append(gevent.spawn(worker_main2))
# g_list.append(gevent.spawn(worker_main3))
# g_list.append(gevent.spawn(worker_main4))
# g_list.append(gevent.spawn(worker_main5))


# while 1:
#     schedule.run_pending()
#     time.sleep(1)
#     print('end once!!!')

# def do_schedule():
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)
#         print('end once!!!')
# queue_thread = threading.Thread(target=do_schedule)
# queue_thread.start()

# gevent.joinall(g_list)

from jobs.test_job import TestJob
from core.base_job import BaseJob
import logging
import abc
import atexit

def hi():
    print('hi, u exit')

logger = logging.getLogger('a')
print(isinstance(TestJob(logger), TestJob))
print(isinstance(TestJob(logger), BaseJob))
print(issubclass(BaseJob, abc.ABCMeta))
print(isinstance(BaseJob(logger), abc.ABCMeta))
print(__name__)
atexit.register(hi)
# BaseJob.register(TestJob)


job_queue = PQueue(20)


def worker_main(worker_no: int):
    print('worker no:', worker_no, ' starting...')
    while 1:
        print('worker no:', worker_no, ' doing...')
        job_func = job_queue.get()
        job_func()

workers = []

for i in range(0, 4):
    # workers.append(threading.Thread(target=worker_main, daemon=True, kwargs={'worker_no': i}))
    # workers[i].start()
    workers.append(Process(target=worker_main, daemon=True, kwargs={'worker_no': i}))
    workers[i].start()


def write_job():
    with open("test.txt", "w") as fp:
        fp.write("hihi")


def send_data():
        while 1:
            with open("test.txt", "w") as fp:
                job_queue.put(lambda :print("hehe"))
                time.sleep(1)


p = Process(target=send_data, daemon=True)
p.start()
p.join()
