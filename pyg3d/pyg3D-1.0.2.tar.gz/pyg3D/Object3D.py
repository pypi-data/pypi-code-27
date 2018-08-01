import numpy as np
import pyglet
from pyglet.gl import *

import pyg3D.Camera as Camera
import pyg3D.Materials as Materials
import pyg3D.ObjectManager as ObjectManager
import pyg3D.Primitive as Primitive
import pyg3D.VectorFunctions as VectorFunctions
import pywavefront as pywavefront


class Object3D :
    """ A class to represent a 3D object.
    """
    def __init__(self,mesh = None, position = (0.0,0.0,0.0), rotation = (0.0,0.0,0.0,0.0), scale = (1.0,1.0,1.0), offset = (0.0,0.0,0.0), primitiveShape = None, textureFile = None, material = None):
        """Initialise a 3D object with a a variety of parameters specifying
        positional information and the desired type of 3D object.

            :Parameters:
                'mesh' : String
                    File url of an .obj mesh to be rendered.
                'position' : (float,float,float)
                    3D position of the object.
                'rotation' : (float angle,float x,float y,float z)
                    Specifies the angle, and axis of an initial rotation for
                    the object.
                'scale' : (float,float,float)
                    The initial scale to be applied to the object.
                'offset' : (float,float,float)
                    An offset to apply to the origin of the object when
                    applying rotations to it.
                'primitiveShape' : :py:class:`~pyg3D.ObjectManager.Shape`
                    If the intention is to render a 3D primitive, this
                    parameter can be set to a :py:class:`~pyg3D.ObjectManager.Shape` enum value to
                    achieve this.
                'textureFile' : String
                    The file url of a texture image file to be applied to
                    the object if it is primitive.
                'material' : function
                    A function from the :py:class:`~pyg3D.Materials` class
                    to set the objects material.


        """
        self.position = position
        self.boundingSphereAdjustmentValue = 1
        if mesh != None:
            self.mesh = pywavefront.Wavefront(mesh)
            #Set bounding sphere adjustment value accordingly for mesh
            print(self.mesh.dimension_min_max())
            dimensionRange = self.mesh.dimension_min_max()

            xSize = dimensionRange[3] - dimensionRange[0]
            ySize = dimensionRange[4] - dimensionRange[1]
            zSize = dimensionRange[5] - dimensionRange[2]

            xCenter = (dimensionRange[3] + dimensionRange[0])/2
            yCenter = (dimensionRange[4] + dimensionRange[1])/2
            zCenter = (dimensionRange[5] + dimensionRange[2])/2



            print("x", xCenter,"y", yCenter, "z", zCenter)

            maxVal = max([xSize,ySize,zSize])
            self.boundingSphereAdjustmentValue = np.sqrt(xSize**2 + ySize**2 + zSize**2)
            print(np.sqrt(xSize**2 + ySize**2 + zSize**2), "max/2",maxVal/2)

        self.rotation = rotation
        self.scale = scale
        self.offset = offset
        self.primitiveShape = primitiveShape
        self.textureFile = textureFile
        self.material = material
        self.trackingClicks = False
        self.collisionMethod = None
        array = []
        self.modelViewMatrix = (GLdouble * 16)(*array)
        self.untransformedModelViewMatrix = (GLdouble * 16)(*array)

        if self.primitiveShape == ObjectManager.Shape.CUBE:
            self.boundingSphereAdjustmentValue = np.sqrt(3)


    def render(self):
        """Add object to a class array for drawing.

        This class array is iterated through every frame."""
        ObjectManager.ObjectManager.meshesToRender.append(self)

    def remove(self):
        """Remove the object from the class array to stop it from
        being drawn."""
        ObjectManager.ObjectManager.meshesToRender.remove(self)

    def registerClickedCallback(self,callback, collisionMethod = ObjectManager.CollisionMethod.ORIENTED_BOUNDING_BOX, button = pyglet.window.mouse.LEFT , modifier = -1):
        """ Enables click detection on the object, calling the specified callback
        when clicked.

            :Parameters:
                'callback' : function
                    A function to be called after the object has been
                    clicked on
                'collisionMethod' : :py:class:`~pyg3D.ObjectManager.CollisionMethod`
                    The method to be used for detecting collisions with the object.
                    Either an oriented bounding box, or a bounding sphere.
                'button' : Int
                    A constant from :py:class:`~pyglet.window.mouse` representing
                    a mouse button to detect clicks with.
                'modifier' : Int
                    If set, clicks will only be detected if a modifier key is
                    being held down. It is a constant from :py:class:`~pyglet.window.key`
                    beginning with MOD
        """
        if collisionMethod == ObjectManager.CollisionMethod.BOUNDING_SPHERE:
            self.trackingClicks = True
            self.clickCallback = callback
            self.collisionMethod = collisionMethod
            self.trackedButton = button
            self.trackedModifier = modifier
        elif collisionMethod == ObjectManager.CollisionMethod.ORIENTED_BOUNDING_BOX:
            self.trackingClicks = True
            self.clickCallback = callback
            self.collisionMethod = collisionMethod
            self.trackedButton = button
            self.trackedModifier = modifier
        else:
            self.trackingClicks = False
            #Fail gracefully for now


    def draw(self):
        """ A draw method to be called by the OpenGL rendering core.
        This method uses the appropriate drawing method depending
        upon the type of object being represented by the Object3D
        object.
        """
        if self.material != None:
            self.material()

        if self.primitiveShape == None and self.mesh != None:
            self.mesh.draw()
            return
        elif self.primitiveShape == ObjectManager.Shape.CUBE:
            if not hasattr(self,"texCube"):
                self.texCube = Primitive.Primitive()
            filePath = ""
            if self.textureFile != None:
                filePath = self.textureFile
            self.texCube.texturableCube( textureImage=filePath)
        elif self.primitiveShape == ObjectManager.Shape.SPHERE:
            if not hasattr(self,"texSphere"):
                self.texSphere = Primitive.Primitive()
            filePath = ""
            if self.textureFile != None:
                filePath = self.textureFile
            self.texSphere.texturableSphere(filePath)
        #Set material back to default
        Materials.Material.defaultMaterial()



    """
    The ray determination and ray-sphere intersection code below, are adapted from the ray-sphere intersection guide
    at http://antongerdelan.net/opengl/raycasting.html and the 
    linked c++ OpenGL 4.0 example at 
    https://github.com/capnramses/antons_opengl_tutorials_book/tree/master/07_ray_picking 
    Author: Anton Gerdelan    
    """
    def rayIntersectionTest(self, clickX, clickY, button, modifiers):
        """ Tests for an intersection with the object at click coordinates
        (clickX,clickY). It does this by casting a ray from the click
        location, through the scene to infinity, and then scene geometry
        is tested via a cuboid or spherical approximation for an intersection
        with this ray.

            :Parameters:
                'clickX' : Int
                    2D X-coordinate of the click.
                'clickY' : Int
                    2D Y-coordinate of the click.
                'button' : Int
                    A constant from :py:class:`~pyglet.window.mouse` representing
                    a mouse button to detect clicks with.
                'modifiers' : Int
                    Clicks will only be detected if a modifier key is
                    being held down. It is a constant from :py:class:`~pyglet.window.key`
                    beginning with MOD

        """
        if not self.trackedButton == button:
            return

        if self.trackedModifier != -1:
            if self.trackedModifier != modifiers:
                return

        x = clickX
        y = clickY
        width = Camera.Camera.width
        height = Camera.Camera.height

        # convert to top left origin
        y = height - y

        x = (2.0 * x) / width - 1.0
        y = 1.0 - (2.0 * y) / height
        z = 1.0

        #Determine clip coordinates
        clip_coords = np.array([x, y, -1.0, 1.0])

        #Retrieve projection matrix
        array = []
        raw_proj_mat = (GLdouble * 16)(*array)
        glGetDoublev(GL_PROJECTION_MATRIX, raw_proj_mat)
        array = np.array(raw_proj_mat)
        projection_matrix = np.reshape(np.matrix(array), (4, 4))

        #Determine eye coordinates
        eye_coords = projection_matrix.I * np.matrix(clip_coords).T
        eye_coords = np.array(eye_coords)
        eye_coords = [eye_coords[0][0], eye_coords[1][0], -1.0, 0.0]

        #Retrieve model view matrix
        raw_view_mat = self.transformationMatrix
        array_mat = np.array(raw_view_mat)
        view_matrix = np.reshape(np.matrix(array_mat), (4, 4))

        #Determine world coordinates
        world_coords = view_matrix.I.T * np.matrix(eye_coords).T
        world_coords = np.array(world_coords)
        world_coords = [world_coords[0][0], world_coords[1][0], world_coords[2][0]]
        world_coords = VectorFunctions.normalise(world_coords)

        #Retrieve campera position from gluUnProject
        array = []

        camera_array = []
        camera_pos = (GLdouble*1)(*camera_array)

        camera_array2 = []
        camera_pos2 = (GLdouble * 1)(*camera_array2)

        camera_array3 = []
        camera_pos3 = (GLdouble * 1)(*camera_array3)

        viewport = (GLint*4)(*array)
        glGetIntegerv(GL_VIEWPORT, viewport)

        gluUnProject((viewport[2] - viewport[0]) / 2.0, (viewport[3] - viewport[1]) / 2.0,
                     0.0, raw_view_mat, raw_proj_mat, viewport,
        camera_pos, camera_pos2, camera_pos3)

        camera_position = (camera_pos[0], camera_pos2[0], camera_pos3[0])

        camera_position = [camera_position[0]*2, camera_position[1]*2, camera_position[2]*2]

        if self.collisionMethod == ObjectManager.CollisionMethod.BOUNDING_SPHERE:

            b = np.dot(np.array(world_coords), camera_position )
            c = np.dot(camera_position, camera_position) - (1*self.boundingSphereAdjustmentValue)**2

            determinant = b * b - c
            if determinant >= 0:
                self.clickCallback()
        elif self.collisionMethod == ObjectManager.CollisionMethod.ORIENTED_BOUNDING_BOX:

            try:
                #Get minimum and maximum bounds for mesh
                minCoord = self.mesh.dimension_min_max()[0:3]
                maxCoord = self.mesh.dimension_min_max()[3:6]
            except AttributeError:
                minCoord = [-0.5,-0.5,-0.5]
                maxCoord = [0.5,0.5,0.5]
            # Retrieve model view matrix
            utransformed_raw_view_mat = self.untransformedModelViewMatrix
            uarray_mat = np.array(utransformed_raw_view_mat)
            uview_matrix = np.reshape(np.matrix(uarray_mat), (4, 4))
            modelMatrix = uview_matrix

            #Subtract given objects offset
            positionTranslationMatrix = [[1, 0, 0, self.position[0] - self.offset[0] ],
                                        [0, 1, 0, self.position[1] - self.offset[1]],
                                        [0, 0, 1, self.position[2] - self.offset[2]],
                                        [0, 0, 0, 1]]

            scalingMatrix = [[self.scale[0]*2,0,0,0],
                             [0,self.scale[1]*2,0,0],
                             [0,0,self.scale[2]*2,0],
                             [0,0,0,1]]

            c = np.cos(np.deg2rad(self.rotation[0]))
            s = np.sin(np.deg2rad(self.rotation[0]))

            x = self.rotation[1]
            y = self.rotation[2]
            z = self.rotation[3]
            axis = VectorFunctions.normalise([x, y, z])
            x = axis[0]
            y = axis[1]
            z = axis[2]

            rotationMatrix = [[(x*x)*(1-c) + c, x*y*(1-c)-z*s, x*z*(1-c) + y*s,0],
                              [x*y*(1-c) + z*s, (y*y)*(1-c) + c, y*z*(1-c) -x*s,0],
                              [x*z*(1-c)-y*s, y*z*(1-c) + x*s, (z*z)*(1-c) + c, 0],
                              [0,0,0,1]]


            # Equivalent to gluLookAt with position and direction of 0,0,0
            zeroMatrix = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 1]]

            zeroMatrix = np.matrix(zeroMatrix)


            negativeOffsetTranslationMatrix = [[1, 0, 0, -self.offset[0]],
                                               [0, 1, 0, -self.offset[1]],
                                               [0, 0, 1, -self.offset[2]],
                                               [0, 0, 0, 1]]

            manualTransformationMatrix = ((modelMatrix.T  @ np.matrix(positionTranslationMatrix ) @ np.matrix(rotationMatrix) @ np.matrix(negativeOffsetTranslationMatrix) @ np.matrix(scalingMatrix)))
            modelMatrix = manualTransformationMatrix

            # Retrieve projection matrix
            array = []
            raw_proj_mat = (GLdouble * 16)(*array)

            glGetDoublev(GL_PROJECTION_MATRIX, raw_proj_mat)
            array = np.array(raw_proj_mat)
            projection_matrix = np.reshape(np.matrix(array), (4, 4))
            eye_coords = projection_matrix.I * np.matrix(clip_coords).T
            eye_coords = np.array(eye_coords)
            eye_coords = [eye_coords[0][0], eye_coords[1][0], -1.0, 0.0]

            #Use calculated model view matrix
            view_matrix = modelMatrix.T
            world_coords = view_matrix.I.T * np.matrix(eye_coords).T
            world_coords = np.array(world_coords)
            world_coords = [world_coords[0][0], world_coords[1][0], world_coords[2][0]]
            world_coords = VectorFunctions.normalise(world_coords)

            offset = np.array(self.offset)
            cam4D = np.append(np.array(Camera.Camera.position) - self.position + offset*2, 1)
            camera_position = np.array(( view_matrix.I.T * zeroMatrix.T *  np.matrix(cam4D).T)[:3].T)[0]
            camera_position = camera_position - offset * 1 / np.array(self.scale)
            # End Duplicate code

            camera_position = [camera_position[0] * 2, camera_position[1] * 2, (camera_position[2] * 2)]

            ray_origin = camera_position
            ray_direction = world_coords

            if self.didRayIntersectCube(minCoord, maxCoord, ray_origin, ray_direction):
                self.clickCallback()

    """
    The following algorithm comes from
    from "Graphics Gems", Academic Press, 1990
    by Andrew Woo. Originally written in C, but rewritten
    in python here
    """
    def didRayIntersectCube(self, minCoord, maxCoord, rayOrigin, rayDirection):
        """ Determines if a given ray intersects a cube defined by its
        maximum and minimum coordinates.

            :Parameters:
                'minCoord' : (float,float,float)
                    The minimum coordinate of the cuboid.
                'maxCoord' : (float,float,float)
                    The maximum coordinate of the cuboid.
                'rayOrigin' : (float,float,float)
                    The origin of the ray for the intersection
                    test to be completed against.
                'rayDirection' : (float,float,float)
                    The vector which represents the direction
                    of the aforementioned ray.

        """
        inside = True
        RIGHT = 0
        LEFT = 1
        MIDDLE = 2

        quadrant = [None,None,None]
        maxT = [None,None,None]
        candidatePlane = [None,None,None]
        coord = [0,0,0]

        #Find candidate planes
        for i in range(3):
            if rayOrigin[i] < minCoord[i]:
                quadrant[i] = LEFT
                candidatePlane[i] = minCoord[i]
                inside = False
            elif rayOrigin[i] > maxCoord[i]:
                quadrant[i] = RIGHT
                candidatePlane[i] = maxCoord[i]
                inside = False
            else:
                quadrant[i] = MIDDLE
        if inside :
            coord = rayOrigin
            return True

        #Calculate t distances to candidate planes
        for i in range(3):
            if quadrant[i] != MIDDLE and rayDirection[i] !=0:
                maxT[i] = [candidatePlane[i] - rayOrigin[i]] / rayDirection[i]
            else:
                maxT[i] = -1

        #Get largest of maxts for final intersection choice
        plane = 0
        for i in range(3):
            if maxT[plane] < maxT[i]:
                plane = i

        #Check final candidate inside box
        if maxT[plane] < 0:
            return False
        for i in range(3):
            if plane != i:
                coord[i] = rayOrigin[i] + maxT[plane] * rayDirection[i]
                if coord[i] < minCoord[i] or coord[i] > maxCoord[i]:
                    return False
            else:
                coord[i] = candidatePlane[i]
        return True
