from collections import namedtuple
from uuid import uuid4
from timer_utils import *

class Actuator():
    def set_state(self, state):
        pass

class RelayControlled(Actuator):
    def __init__(self, pin):
        self.pin = pin

    def set_state(self, state):
        pass

    def turn_on(self):
        self.set_state(True)

    def turn_off(self):
        self.set_state(False)

    def change_to_for(self, s, time, state):
        self.set_state(state)
        def stop(*args, **kwargs):
            self.set_state(not state)
        return run_after(s, time, stop)

    def turn_on_for(self, s, time):
        return self.change_to_for(s, time, True)

    def turn_off_for(self, s, time):
        return self.change_to_for(s, time, False)

    def cycle(self, s, frac_on, duration):
        return cycle_on_off(s, self.set_state, frac_on, duration)




class LEDs(RelayControlled):
    pass

class Fan(RelayControlled):
    pass

class Pump(RelayControlled):
    pass
