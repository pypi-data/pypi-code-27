
class LightGrouping:
    def __init__(self, lights=[]):
        self.lights = lights

    def add_light(self, light):
        self.lights.append(light)

    def turn_on(self):
        for light in self.lights:
            light.turn_on()

    def turn_off(self):
        for light in self.lights:
            light.turn_off()
