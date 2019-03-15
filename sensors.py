from collections import namedtuple
from random import random


class Sensor():
    def sense(self):
        pass

class GPIOSensor(Sensor):
    def __init__(self, pin):
        self.pin = pin

class TemperatureAndHumidity(GPIOSensor):
    def sense(self):
        return random() * 30, random() * 100

class SoilHumidity(GPIOSensor):
    def sense(self):
        return random() * 100

class Camera(Sensor):
    def __init__(self, number):
        self.number = number

    def sense(self):
        return None

class SensorHub():
    def __init__(self):
        self.temp_and_hum = TemperatureAndHumidity(TEMPERATURE_PIN)
        self.soil_humidity = SoilHumidity(SOIL_HUM_PIN)
        self.camera = Camera(CAMERA_NUMBER)
        self.values = {}

    def get_value(self, key):
        if key in ['temperature','humidity']:
            # if the temperature information can be gotten from the memoized values
            if ('temp_and_hum' in self.values and 
                    self.values['temp_and_hum'][key] is not None):
                tah = self.values['temp_and_hum']
            else: 
                t, h = self.temp_and_hum.sense()
                tah = {
                    'temperature': t,
                    'humidity': h
                }
            val, tah[key] = tah[key], None # some fun python syntax that I just had to do
            self.values['temp_and_hum'] = tah
            return val
        if key == 'soil_humidity':
            val = self.soil_humidity.sense()
            self.values['soil_humidity'] = val
            return val
        if key in ['camera', 'image', 'color_image']:
            val = self.camera.sense()
            self.values['image'] = val
            return val
        if key in ['green_image']:
            print('not implemented yet', key)
            return None
        else:
            print('invalid key', key)
            return None






TEMPERATURE_PIN = 20
SOIL_HUM_PIN = 21
CAMERA_NUMBER = 0
