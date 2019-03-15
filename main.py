from sched import scheduler
import time
from actuators import *
from timer_utils import *
import datetime
from sensors import *
from data_logging import FileLogger

last_sensor_state = None



def read_sensors(logger, *args, **kwargs):
    global last_sensor_state
    last_sensor_state = get_sensor_state()
    logger.log(last_sensor_state)

def cool_box(*args, **kwargs):
    global last_sensor_state
    if target_temp < last_sensor_state.temperature:
        print('box too hot turning on fan')
        set_fan_state(True)
    else:
        set_fan_state(False)

def add_water(*args, **kwargs):
    global last_sensor_state
    if target_soil_humidity > last_sensor_state.soil_humidity:
        print('box too dry turning on pump')
        turn_pump_on_for(s, 1*seconds)


def main():

    s = scheduler(time.time, time.sleep)

    with FileLogger('sensors', headers=SensorsState) as logger:
        every(s, 5*seconds, read_sensors, args=(logger,), priority=1)
        every(s, 5*seconds, cool_box, priority=2)
        every(s, 10*seconds, add_water, priority=2)
        s.run()

if __name__ == '__main__':
    main()