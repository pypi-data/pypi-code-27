from pyglet.gl import *
from pyglet import image

class Primitive():
    """A simple class defining texture ready primitive 3D shapes"""


    def texturableCube(self, textureImage = ""):
        """ Draws a texture mapped cube

            :Parameter:
                'textureImage' : String
                        The file URL of an image file to be applied to the primitive as a texture

        """
        if textureImage != "":
            if not hasattr(self,"sphereTexture") :
                self.sphereTexture = image.load(textureImage)
            glEnable(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glBindTexture(self.sphereTexture.texture.target, self.sphereTexture.texture.id)

            #glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA, texture.width, texture.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture.get_image_data())

        glPushMatrix()
        glScalef(1/2.0,1/2.0,1/2.0)

        normals = [[1.0,0.0,0.0],[-1.0,0.0,0.0],[0.0,0.0,1.0],[0.0,0.0,-1.0],[0.0,-1.0,0.0],[0.0,1.0,0.0]]
        normals_gl = []
        for normalList in normals:
            normals_gl.append((GLfloat * len(normalList))(*normalList))

        glNormal3fv(normals_gl[0])
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1, 0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(0, 1)
        glVertex3f(1.0, 1.0, 1.0)
        glEnd()

        glNormal3fv(normals_gl[3])
        glBegin(GL_POLYGON)
        glTexCoord2f(1, 0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0, 0)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(0, 1)
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(-1.0, 1.0, -1.0)
        glEnd()

        glNormal3fv(normals_gl[2])
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1, 0)
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1, 1)
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex3f(-1.0, 1.0, 1.0)
        glEnd()

        glNormal3fv(normals_gl[1])
        glBegin(GL_POLYGON)
        glTexCoord2f(1, 0)
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(0, 0)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(0, 1)
        glVertex3f(-1.0, 1.0, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(-1.0, 1.0, 1.0)
        glEnd()

        glNormal3fv(normals_gl[5])
        glBegin(GL_POLYGON)
        glTexCoord2f(1, 0)
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(1, 1)
        glVertex3f(1.0, 1.0, -1.0)
        glTexCoord2f(0, 1)
        glVertex3f(-1.0, 1.0, -1.0)
        glTexCoord2f(0, 0)
        glVertex3f(-1.0, 1.0, 1.0)
        glEnd()

        glNormal3fv(normals_gl[4])
        glBegin(GL_POLYGON)
        glTexCoord2f(0, 0)
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(0, 1)
        glVertex3f(1.0, -1.0, -1.0)
        glTexCoord2f(1, 1)
        glVertex3f(-1.0, -1.0, -1.0)
        glTexCoord2f(1, 0)
        glVertex3f(-1.0, -1.0, 1.0)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def texturableSphere(self, texture = ""):
        """ Draws a texture mapped sphere

            :Parameter:
                'textureImage' : String
                        The file URL of an image file to be applied to the primitive as a texture

        """
        glPushMatrix()
        q = gluNewQuadric()
        if texture != "":
            if not hasattr(self,"sphereTexture") :
                self.sphereTexture = image.load(texture)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.sphereTexture.texture.id)
            gluQuadricDrawStyle(q, GLU_FILL)
            gluQuadricTexture(q, GL_TRUE)
            gluQuadricNormals(q, GLU_SMOOTH)
            glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        gluSphere(q,0.5,50,50)
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
