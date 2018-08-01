from enum import Enum
class Shape(Enum):
    """ An enum representing the 2 primitive shapes defined
    in the library. The cube and the sphere.
    """
    CUBE = 1
    SPHERE = 2
class LightType():
    DIRECTIONAL = 0
    SPOTLIGHT = 1
class CollisionMethod (Enum):
    """ An enum representing the different methods available
    for approximating 3D geometry for click detection.
    Namely oriented bounding box and bounding sphere.
    """
    ORIENTED_BOUNDING_BOX = 1
    BOUNDING_SPHERE = 2

class ObjectManager :
    """Maintain global arrays of 2D and 3D objects to render."""

    meshesToRender = []
    pygletObjectsToRender = []
    lightsToRender = []



