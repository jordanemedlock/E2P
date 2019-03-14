from collections import namedtuple
from uuid import uuid4
from timer_utils import *

def set_led_state(state):
    print('LED state set to: ' + str(state))

def set_fan_state(state):
    print('fan state set to: ' + str(state))

def set_pump_state(state):
    print('pump state set to: ' + str(state))

class ActuatorsState(namedtuple('ActuatorsState', ['led', 'fan', 'pump'])):
    pass

def set_actuators_state(actuators_state):
    set_led_state(actuators_state.led)
    set_fan_state(actuators_state.fan)
    set_pump_state(actuators_state.pump)

def cycle_led(scheduler, frac_on, frequency):
    return cycle_on_off(scheduler, set_led_state, frac_on, frequency)

def cycle_fan(scheduler, frac_on, frequency):
    return cycle_on_off(scheduler, set_fan_state, frac_on, frequency)

def cycle_pump(scheduler, frac_on, frequency):
    return cycle_on_off(scheduler, set_pump_state, frac_on, frequency)

def turn_pump_on_for(s, time):
    set_pump_state(True)
    def stop(*args, **kwargs):
        set_pump_state(False)
    return run_after(s, time, stop)
