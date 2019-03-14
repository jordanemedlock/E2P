import pytz
import datetime as dt
import time
from uuid import uuid4

tz = pytz.timezone("America/Los_Angeles")

def cycle_on_off(s, func, frac_on, frequency):
    cycle_id = str(uuid4())
    on_time = frequency * frac_on
    off_time = frequency * (1 - frac_on)

    def turn_on(*args, **kwargs):
        func(True)
        s.enter(on_time, 2, turn_off, kwargs={'cycle_id': cycle_id})

    def turn_off(*args, **kwargs):
        func(False)
        s.enter(off_time, 2, turn_on, kwargs={'cycle_id': cycle_id})

    turn_on()

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


def at_time(s, task, time_of_day, priority=5, arguments=(), kwargs={}):
    global tz
    today = dt.date.today()
    now = dt.datetime.now()
    possible = dt.datetime.combine(today, time_of_day)
    if now > possible:
        tomorrow = today + dt.timedelta(days=1)
        possible = dt.datetime.combine(tomorrow, time_of_day)

    t = time.mktime(possible.timetuple())
    return s.enterabs(t, priority, task, argument=arguments, kwargs=kwargs)

def daily(s, task, time_of_day, priority=5, arguments=(), kwargs={}):
    def tick(*args, **kwargs):
        task(*args, **kwargs)
        at_time(s, tick, time_of_day, priority, args, kwargs)

    kwargs['cycle_id'] = str(uuid4())
    at_time(s, tick, time_of_day, priority, arguments, kwargs)










