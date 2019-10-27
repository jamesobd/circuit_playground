"""
@Author Scott Jensen & James Jensen
@Copyright: MIT

CRON Job runner
Add CRON job functions and have them run at the specified interval in seconds
NOTE:  Be sure to run the next() function somewhere in your main program loop
"""

### Import statements
import time
# import pydash as py_
jobs = []
last_id = None

def next():
    for job in jobs:
        if job['lastTime'] + job['interval'] < time.monotonic():
            intervalTimes = (time.monotonic() - job['lastTime']) // job['interval']
            job['lastTime'] += job['interval'] * intervalTimes
            job['fn']()

"""
Example use:

import cron
def twoSecondJob():
    print("I run every 2 seconds")
cron.add(oneSecondJob, 2)
"""
def add(fn, sec, id=None):
    global last_id
    if (last_id is None):
        last_id = 0
    else:
        last_id += last_id + 1

    jobs.append({'id': id or last_id, 'fn': fn, 'interval': sec, 'lastTime': time.monotonic()})

def remove(id):
    """A special data class with validation and transitions"""
    #print('delete:', job['id'])