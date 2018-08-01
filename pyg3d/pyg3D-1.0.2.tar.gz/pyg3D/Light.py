from pyglet.gl import *
import pyg3D.ObjectManager as ObjectManager

class Light :
    """A class which allows the specification of Lights
        via their parameters
    """
    numberOfLights = 0

    def __init__(self, position = (0,0,1), specular = (1,1,1,1), diffuse = (1,1,1,1), type = ObjectManager.LightType.DIRECTIONAL,
                 ambient = (0,0,0,1), spot_direction = (0,0,-1), spot_exponent = 0, spot_cutoff = 180,
                 constant_attenuation = 1, linear_attenuation = 0, quadratic_attenuation = 0):
        """
        Initialises an OpenGL light

        :Parameters:
            'position' : (float,float,float)
                The position of the light
            'specular' : (float,float,float,float)
                The specular component of the light
            'diffuse' : (float,float,float,float)
                The diffuse component of the light
            'type' : :py:class:`~pyg3D.ObjectManager.LightType`
                The type of the light, either SPOT or DIRECTIONAL.
            'ambient' : (float,float,float,float)
                The ambient component of the light
            'spot_direction' : (float,float,float)
                The direction of light for a spot light
            'spot_exponent' : float
                A value in the range 0-128
                Higher values result in a more focused light
            'spot_cutoff' : float
                A value in the range 0-90 or 180
                Specifies the angle between the direction of the
                light and its target at which it will cutoff.
                180 results in no cutoff
            'constant_attenuation' : float
                The constant attenuation factor
            'linear_attenuation' :  float
                The linear attenuation factor
            'quadratic_attenuation' : float
                The quadratic attenuation factor

        """
        self.position = position
        self.specular = specular
        self.diffuse = diffuse
        self.type = type
        self.lightNum = Light.numberOfLights
        self.ambient = ambient
        self.spot_direction = spot_direction
        self.spot_exponent = spot_exponent
        self.spot_cutoff = spot_cutoff
        self.constant_attenuation = constant_attenuation
        self.linear_attenuation = linear_attenuation
        self.quadratic_attenuation = quadratic_attenuation

        if Light.numberOfLights == 0:
            Light.defaultLight = self
        if Light.numberOfLights > 8:
            raise ValueError("The maximum number of lights in OpenGL is 8")


    def getDefaultLight(self):
        """ Get the default light already setup by the library

        """
        return Light.defaultLight

    def render(self):
        """Add light to a class array for rendering"""
        ObjectManager.ObjectManager.lightsToRender.append(self)
        Light.numberOfLights +=1

    def remove(self):
        """Remove light from the class array to stop rendering"""
        ObjectManager.ObjectManager.lightsToRender.remove(self)
        Light.numberOfLights -= 1