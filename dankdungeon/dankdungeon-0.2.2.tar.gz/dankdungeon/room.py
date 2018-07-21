'''
Room generator

Attributes
----------

- amount of light
- smell
- dustiness
- sounds
- wind, breeze, draft
- echoes
- what are walls made of
- what is ceiling made of
- how tall is the ceiling
- what is floor made of
- size of the room
- is there rubble
- wetness, humidity
- temperature of the room
- feeling of evil, being watched
- dripping from ceiling
- are there footprints, do you leave footprints
- do you make a sound when you walk through
- is there writing on the walls or floor or ceiling
'''


class Room:

    def __init__(self, **kwargs):
        for arg, val in kwargs.items():
            setattr(self, arg, val)
