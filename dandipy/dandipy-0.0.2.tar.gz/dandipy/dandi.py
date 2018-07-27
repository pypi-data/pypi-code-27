import requests
import json

token = "MEDQ5xp/hAlwDei/yjIB2AlB38LRfEoVw9l40ge7tVO812AJ1oBn1wF7sAX9/uqN04K0hIbclbI//FIrFQrg6uWZk75yFI6LGO3sQ7EgOJAuBWuFFQfvKf8ZxBoRif3BvNPx3au68NAhH/UdP0jMqCOZ3Dnkp0DpaNpYUwS1nM8vNeC6l96tt8f0e0GW/3UtSaBg4PzK5SU8FTlXLCyL+YpObBmdrirCb5VsWy1nAbLkFESaVXEmwKOSB59kd"

base_uri = "https://www.momentoftop.com/dnd/v0/"

class Character:
    def __init__(self, name):
        self.name = name
        self.all_characters = requests.get(base_uri + "characters",
                        headers={'Authorization':token}).json()

    def create_character(self, char_class, alignment):
        self.char_class = char_class
        self.alignment = algnment
        payload = {
            'name':name,
            'charClass':char_class,
            'alignment':alignment,
            }
        
        return requests.put(base_uri + "characters",
                            data = json.dumps(payload),
                            headers={'Authorization':token})

    def get_character(self):
        attributes = requests.get(base_uri + "characters/" + self.name,
                            headers={'Authorization':token}).json()
        return attributes

    def attack(self, enemy):
        payload = {"defender": enemy}
        
        return requests.post(base_uri + "characters/" + self.name.replace(" ","%20") + "/attack",
                            data = json.dumps(payload),
                            headers={'Authorization':token})
    
        










