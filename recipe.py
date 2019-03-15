import json
from collections import namedtuple
import jsonpickle

recipe_super = namedtuple('Recipe', [
    'name', 
    'description', 
    'temperature', 
    'soil_humidity', 
    'light_frac'
])

class Recipe():
    def __init__(self, name, description, temperature, soil_humidity, light_frac):
        self.name = name
        self.description = description
        self.temperature = temperature
        self.soil_humidity = soil_humidity
        self.light_frac = light_frac

    def open(filename):
        with open(filename, 'r') as f:
            return jsonpickle.decode(f.read())

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(jsonpickle.encode(self))

def test():
    r = Recipe(
        name='Basil', 
        description='Grows basil pretty well idk', 
        temperature=25, 
        soil_humidity=25,
        light_frac=0.5
    )
    r.save('recipes/Basil.json')

    basil = Recipe.open('recipes/Basil.json')
    print(basil)


if __name__ == '__main__':
    test()
