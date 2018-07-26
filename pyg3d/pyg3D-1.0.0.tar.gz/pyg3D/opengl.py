#!/usr/bin/env python
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

''' Main OpenGL rendering logic for the library

Here 3D and 2D rendering is performed for the library. It is not designed to
be used directly, but indirectly through other library functions.

'''

from pyglet.gl import *
from OpenGL.GLUT import *
import pyglet
import pyg3D.ObjectManager as ObjectManager
import numpy as np
import pyg3D.Camera as Camera


class pyg3D(pyglet.window.Window):
    """ Class which performs OpenGL rendering for the library.
    It is a subclass of a pyglet window, overriding resize, draw and mouse press events.

    """

    def on_resize(self,width, height):
        """
        Overridden :py:meth:`~pyglet.window.Window.on_resize` method
        This changes the viewport as window is scaled to match new
        dimensions.
        This also updates the :py:class:`~pyg3D.Camera` class attributes to reflect the
        new width and height.

        It ensures the lights are positioned correctly, and that the
        perspective projection matrix is set up with the correct
        aspect ratio.

        :Parameters:
            'width' : int
                    The new width in pixels of the window.
            'height' : int
                    The new height in pixels of the window

        """
        # Override the default on_resize handler to create a 3D projection
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        Camera.Camera.width = width
        Camera.Camera.height = height
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Define a simple function to create ctypes arrays of floats:
        def vec(*args):
            return (GLfloat * len(args))(*args)

        glLightfv(GL_LIGHT0, GL_POSITION, vec(0., 0., 10, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))

        glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

        # get into projection matrix and set the camera
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(Camera.Camera.fovy, max(1, width) / float(max(1, height)), Camera.Camera.near, Camera.Camera.far)

        #glOrtho((width / height) * -4.0, (width / height) * 4.0, -4.0, 4.0, -20.0, 20.0)
        print("width height", width, height)
        glMatrixMode(GL_MODELVIEW)

        self.setCameraPosition()
        return pyglet.event.EVENT_HANDLED





    def on_draw(self):
        """ Overridden :py:meth:`~pyglet.window.Window.on_draw` method to perform OpenGL drawing
            Draws objects from class arrays storing 3D and 2D objects.

            Performs transformations for each drawn object depending upon their
            scale, rotation and position variables.

            Additionally it switches between perspective and orthographic
            projection matrices for 3D and 2D objects respectively.
            """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(Camera.Camera.fovy, max(1, Camera.Camera.width) / float(max(1, Camera.Camera.height)), Camera.Camera.near, Camera.Camera.far)
        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity()

        # Change light positions here in future

        glPopMatrix()

        # get in mode for drawing
        glMatrixMode(GL_MODELVIEW)

        # Prevents scaling of normals
        glEnable(GL_NORMALIZE)
        # Draw here
        for object in ObjectManager.ObjectManager.meshesToRender:

            glPushMatrix()

            # Set initial transformation matrix if needed
            if object.trackingClicks == True:
                array = []
                raw_view_mat = (GLdouble * 16)(*array)
                glGetDoublev(GL_MODELVIEW_MATRIX, raw_view_mat)
                object.untransformedModelViewMatrix = raw_view_mat

            # Translate to correct position for object
            glTranslatef(object.position[0], object.position[1], object.position[2])

            # For rotational offset, translate away from origin
            glTranslatef(-object.offset[0], -object.offset[1], -object.offset[2])

            # Rotate to correct rotation for object
            glRotatef(object.rotation[0], object.rotation[1], object.rotation[2], object.rotation[3])

            # For rotational offset, translate back to origin
            glTranslatef(+object.offset[0], +object.offset[1], +object.offset[2])



            # Scale to objects scale values
            glScalef(object.scale[0], object.scale[1], object.scale[2])

            # Set transformed model view matrix if needed
            if object.trackingClicks == True:
                array = []
                raw_view_mat = (GLdouble * 16)(*array)
                glGetDoublev(GL_MODELVIEW_MATRIX, raw_view_mat)
                object.transformationMatrix = raw_view_mat

            # If camera has a target, set it to look at targets position
            if Camera.Camera.target == object:
                Camera.Camera.lookAt = object.position

            """
            #DEBUG PRINT
            if object.primitiveShape == ObjectManager.Shape.CUBE:
                array2 = []
                raw_view_mat2 = (GLdouble * 16)(*array2)
                glGetDoublev(GL_MODELVIEW_MATRIX, raw_view_mat2)
                array_mat = np.array(raw_view_mat2)
                view_matrix = np.reshape(np.matrix(array_mat), (4, 4))
                print("cube mat")
                print(view_matrix)
                print("cube mat")
            """


            object.draw()
            glPopMatrix()

        # Disable lighting for 2D drawing
        glDisable(GL_LIGHTING)
        # Select projection matrix
        glMatrixMode(GL_PROJECTION)
        # Save its current state
        glPushMatrix()
        # Set it to default identity matrix
        glLoadIdentity()
        # Use orthographic projection matrix for 2D projection
        glOrtho(0.0, max(1, Camera.Camera.width), max(1, Camera.Camera.height), 0.0, -1.0, 4.0)
        # Select model view matrix for drawing
        glMatrixMode(GL_MODELVIEW)
        # Set it to default identity matrix
        glLoadIdentity()

        # Flip 2D rendering to correct side
        glScalef(1, -1, 1)

        # Draw all 2D pyglet objects
        for object in ObjectManager.ObjectManager.pygletObjectsToRender:
            object.object.draw()

        # Set projection matrix back to saved state
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        # Select model view matrix
        glMatrixMode(GL_MODELVIEW)
        # Re-enable disabled lighting for 3D drawing
        glEnable(GL_LIGHTING)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.setCameraPosition()

    def on_mouse_press(self,x, y, button, modifiers):
        """ Override :py:meth:`~pyglet.window.Window.on_mouse_press` method
            to perform any ray intersection tests for objects registered
            to receive click callbacks.
        """
        for object in ObjectManager.ObjectManager.meshesToRender:
            if object.trackingClicks == True:
                object.rayIntersectionTest(x,y, button, modifiers)

    def setCameraPosition(self):
        """
        Retrieves camera position information from :py:class:`~Camera` class
        attributes.
        This then uses this information to call glulookAt() with these parameters
        """
        pos = Camera.Camera.position
        lookAt = Camera.Camera.lookAt
        upDir = Camera.Camera.upDir
        #Position, look at, up dir
        gluLookAt(pos[0], pos[1], pos[2], lookAt[0], lookAt[1], lookAt[2], upDir[0], upDir[1], upDir[2])

    def setup(self):
        """ Sets up OpenGL drawing. Defines and enables basic lighting for the
            scene.

        """
        # One-time GL setup
        glClearColor(0.0, 0.0, 0.0, 0)
        # glColor3f(1, 0, 0)
        glEnable(GL_DEPTH_TEST)
        #glEnable(GL_CULL_FACE)

        # Uncomment this line for a wireframe view
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
        # but this is not the case on Linux or Mac, so remember to always
        # include it.
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Define a simple function to create ctypes arrays of floats:
        def vec(*args):
            return (GLfloat * len(args))(*args)

        glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))

        glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 1, 1, 1))

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True, )
    window = pyg3D(resizable=True, config=config)
except:
    # Fall back to no multisampling for old hardwares
    try:
        window = pyg3D(resizable=True)
    except:
        window = None
if window != None:
    window.setup()