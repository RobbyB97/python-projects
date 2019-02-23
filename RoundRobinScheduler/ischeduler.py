"""
    Round Robin Scheduler
    Author: Robert Bergers
    results = 'records.txt'
    logs = 'log.txt'
"""

import logging as log
from queue import Queue
import threading as th
from time import time, sleep
from random import randint

quan = 1
cs = 0
c = 0
avgturnaround = 0
list = []

# The do process method executes the simulated processing on the
# thread. Returns true if the thread is completed.

def doprocess(proc):
    global avgturnaround
    global list
    addwait = lambda x: x['wait'] + (c - x['replaced'])
    l.acquire()
    try:
        if not proc['rem']:
            proc['initial wait'] = c
        for i in range(0, quan):
            if proc['rem'] != proc['service']:
                sleep(1)
                proc['rem'] += 1
            else:
                proc['finaltime'] = c
                f = open('records.txt', 'a')
                proc['turnaround'] = c - proc['arrival']
                avgturnaround += proc['turnaround']
                f.close()
                list.append(proc)
                return True
        proc['wait'] = addwait(proc)
        proc['put'] = c
    finally:
        proc['replaced'] = c
        l.release()
    return False

# The round robin method will pull threads from the queue and
# call the do process method to be performed on the thread. If the do
# process method returns False, it will put it back in the queue. If True,
# it will complete the task.

def roundrobin():
    simulating = True
    i = 0
    while True:
        proc = q.get()
        log.info('got')
        if doprocess(proc):
            log.info('Process %s completed' % proc['id'])
            q.task_done()
            i += 1
        else:
            log.info('Process %s back in queue' % proc['id'])
            q.put(proc)
        if q.empty() and i > 10:
            simulating = False
        if cs > 0:
            sleep(cs)
    return

# The scheduler method will create a thread for each process at
# A random interval and will call the round robin method on those
# threads to simulate scheduling them. Once all the processes are
# completed, it gives the total simulated time and writes to the log

def scheduler():
    global c
    global list
    global avgturnaround
    iat = lambda: randint(4, 8)
    sert = lambda: randint(5, 10)
    proctotal = int(input('Enter number of processes: '))
    for i in range(0, proctotal):
        t = th.Thread(name='Process %s' % i, target=roundrobin)
        t.setDaemon = True
        t.start()
        proc = {
            'id': i, 'arrival': c, 'service': sert(), 'rem': 0, 'wait': 0,
            'replaced': 0
        }
        log.info('Created Process [%s]' % i)
        q.put(proc)
        for j in range(0, iat()):
            sleep(1)
            c += 1
            log.info('cycle')
    while proctotal > len(list):
        sleep(1)
    avgturnaround = avgturnaround / proctotal
    log.info('Simulation took %s seconds to finish' % c)
    f = open('log.txt', 'w')
    for item in list:
        f.write('Process %s: ' % item['id'])
        for key, value in item.items():
            if key in {'rem', 'put', 'replaced'}:
                pass
            else:
                f.write('[%(key)s]%(value)d | ' %
                        {'key': key, 'value': value})
        f.write('\n')
    f.write('Average turnaround time: %s' % int(avgturnaround))
    f.close()
    return

# The main method will create the necessary objects to schedule the
# threads, initialize the logger and open records. It will then call the
# scheduler loop.

if __name__ == '__main__':
    globals()
    l = th.Lock()
    q = Queue()
    log.basicConfig(filename='log.txt', level=log.INFO)  # Log
    logFormatter = log.Formatter("\n %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = log.getLogger()
    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(20)
    f = open('records.text', 'w')
    f.close()
    scheduler()
