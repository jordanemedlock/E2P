import pytz
import datetime as dt
import time
from uuid import uuid4

tz = pytz.timezone("America/Los_Angeles")

seconds = 1

minutes = 60 * seconds

hours = 60 * minutes

days = 24 * hours

def cycle(s, func, time_diff, priority=5, args=(), kwargs={}):
    cycle_id = str(uuid4())
    def call_func(*args, **kwargs):
        s.enter(time_diff, priority, call_func, args, kwargs)
        func(*args, **kwargs)

    kwargs['cycle_id'] = cycle_id
    call_func(*args, **kwargs)

    return cycle_id

def every(s, time_diff, func, priority=5, args=(), kwargs={}):
    return cycle(s, func, time_diff, priority=5, args=args, kwargs=kwargs)


def cycle_on_off(s, func, frac_on, time_diff, priority=5, args=(), kwargs={}):
    cycle_id = str(uuid4())
    on_time = time_diff * frac_on
    off_time = time_diff * (1 - frac_on)

    def turn_on(*args, **kwargs):
        s.enter(on_time, 2, turn_off, arguments=args, kwargs=kwargs)
        func(True)

    def turn_off(*args, **kwargs):
        s.enter(off_time, 2, turn_on, arguments=args, kwargs=kwargs)
        func(False)

    kwargs['cycle_id'] = cycle_id
    turn_on(*arguments, **kwargs)

    return cycle_id

def stop_cycle(s, cycle_id):
    event = None
    for ev in s.queue:
        if 'cycle_id' in ev.kwargs and ev.kwargs['cycle_id']:
            event = ev

    if event:
        s.cancel(event)
        return True
    return False


def at_time(s, task, time_of_day, priority=5, args=(), kwargs={}):
    global tz
    today = dt.date.today()
    now = dt.datetime.now()
    possible = dt.datetime.combine(today, time_of_day)
    if now > possible:
        tomorrow = today + dt.timedelta(days=1)
        possible = dt.datetime.combine(tomorrow, time_of_day)

    t = time.mktime(possible.timetuple())
    return s.enterabs(t, priority, task, argument=args, kwargs=kwargs)

def every_day_at(s, time_of_day, task, priority=5, args=(), kwargs={}):
    def tick(*args, **kwargs):
        task(*args, **kwargs)
        at_time(s, tick, time_of_day, priority, args, kwargs)

    kwargs['cycle_id'] = str(uuid4())
    at_time(s, tick, time_of_day, priority, args, kwargs)


def run_after(s, time_diff, task, priority=5, args=(), kwargs={}):
    cycle_id = str(uuid4())
    kwargs['cycle_id'] = cycle_id
    s.enter(time_diff, priority, task, args, kwargs)
    return cycle_id



def after(s, time_diff, task, priority=5, args=(), kwargs={}):
    cycle_id = str(uuid4())
    kwargs['cycle_id'] = cycle_id
    s.enter(time_diff, priority, task, args, kwargs)
    return cycle_id






