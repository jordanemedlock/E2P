import sys
sys.path.append("..")

from timer_utils import *
from actuators import LEDs, Fan, Pump
from sensors import TemperatureAndHumidity, SoilHumidity, Camera
from data_logging import FileLogger
import datetime

leds = LEDs(2, active_high=False)
fan = Fan(3, active_high=False)
pump = Pump(4, active_high=False)
temp_and_hum = TemperatureAndHumidity(20)
soil = SoilHumidity(20)
camera = Camera(20)
print(temp_and_hum)

target_temp = 25
target_soil_hum = 50
last_measurements = {}

def log_sensors(log, *args, **kwargs):
    global last_measurements, temp_and_hum, soil
    print('logging sensors')
    t, h = temp_and_hum.sense()
    s = soil.sense()
    last_measurements = {
        'temperature': t,
        'humidity': h,
        'soil_humidity': s
    }
    log.log(last_measurements)

def regulate_temperature(*args, **kwargs):
    global last_measurements, fan
    if last_measurements['temperature'] > target_temp:
        print('turning fan on')
        fan.turn_on()
    else:
        print('turning fan off')
        fan.turn_off()

def water_plant(s, *args, **kwargs):
    global last_measurements, pump
    if last_measurements['soil_humidity'] < target_soil_hum:
        pump.turn_on_for(s, 1*seconds)
        after(s, 10*seconds, water_plant, args=(s,))

def turn_on_lights(*args, **kwargs):
    leds.turn_on()

def turn_off_lights(*args, **kwargs):
    leds.turn_off()

def run(s):

    file_logger = FileLogger('basil', headers=['temperature', 'humidity', 'soil_humidity'])
    with file_logger:
        every(s, 5*seconds, log_sensors, args=(file_logger,))
        every(s, 5*seconds, regulate_temperature)

        every_day_at(s, datetime.time(20, 0, 0), water_plant, args=(s,))

        every_day_at(s, datetime.time(6, 0, 0), turn_on_lights)
        every_day_at(s, datetime.time(18, 0, 0), turn_off_lights)

        yield None

