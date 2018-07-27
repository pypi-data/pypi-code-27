
class Light:
    def __init__(self, pin_num, gpio):
        self.pin_num = pin_num
        self.gpio = gpio
        self.gpio.setup(self.pin_num, self.gpio.OUT)
        self.state = False

    def turn_on(self):
        if not self.state:
            self.gpio.output(self.pin_num, True)
            self.state = True

    def turn_off(self):
        if self.state:
            self.gpio.output(self.pin_num, False)
            self.state = False
