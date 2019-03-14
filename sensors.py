from collections import namedtuple
from random import random

TEMPERATURE_PIN = 20
SOIL_HUM_PIN = 21
CAMERA_NUMBER = 0

def get_temperature_and_humidity():
    return random() * 30, random() * 100

def get_soil_humidity():
    return random() * 100

def get_image():
    return None

class SensorsState(namedtuple('SensorsState', ['temperature', 'humidity', 'soil_humidity', 'image'])):
    pass

def get_sensor_state():
    t, h = get_temperature_and_humidity()
    sh = get_soil_humidity()
    i = get_image()
    return SensorsState(t, h, sh, i)

