from pyglet.gl import *
import pyg3D.ObjectManager as ObjectManager

class Object2D :
    """Represents a 2D drawable pyglet object"""
    def __init__(self,object):
        """
            :Parameter:
                'object' : Any pyglet object which implements draw() method
        """
        self.object = object


    def render(self):
        """Add 2D pyglet object to a class array for drawing"""
        ObjectManager.ObjectManager.pygletObjectsToRender.append(self)

    def remove(self):
        """Remove 2D pyglet object from a class array to stop drawing"""
        ObjectManager.ObjectManager.pygletObjectsToRender.remove(self)

    def draw(self):
        self.object.draw()