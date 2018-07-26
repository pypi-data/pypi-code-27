from pyglet.gl import *

class Material():
    """Static class encapsulating OpenGL material changes

    Calling one of it's static methods immediately changes
    OpenGL material properties.
    Providing a convenient way to change materials.
    """
    @staticmethod
    def brassMaterial():
        """Change ambient, diffuse, specular and highlight components of light
            to mimic brass
        """
        ambient = [0.33, 0.22, 0.03, 1.0]
        ambient_gl = (GLfloat * len(ambient))(*ambient)

        diffuse = [0.78, 0.57, 0.11, 1.0]
        diffuse_gl = (GLfloat * len(diffuse))(*diffuse)

        specular = [0.99, 0.91, 0.81, 1.0]
        specular_gl = (GLfloat * len(specular))(*specular)

        highlight = 0.21*128
        highlight_gl = GLfloat(highlight)

        glMaterialfv(GL_FRONT, GL_AMBIENT,ambient_gl);
        glMaterialfv(GL_FRONT, GL_DIFFUSE,diffuse_gl);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_gl);
        glMaterialf(GL_FRONT, GL_SHININESS, highlight_gl);

    @staticmethod
    def emeraldMaterial():
        """Change ambient, diffuse, specular and highlight components of light
            to mimic emerald
        """
        ambient = [0.022, 0.17, 0.02, 1.0]
        ambient_gl = (GLfloat * len(ambient))(*ambient)

        diffuse = [0.08, 0.6, 0.08, 1.0]
        diffuse_gl = (GLfloat * len(diffuse))(*diffuse)

        specular = [0.63, 0.73, 0.63, 1.0]
        specular_gl = (GLfloat * len(specular))(*specular)

        highlight = 0.6*128
        highlight_gl = GLfloat(highlight)

        glMaterialfv(GL_FRONT, GL_AMBIENT,ambient_gl);
        glMaterialfv(GL_FRONT, GL_DIFFUSE,diffuse_gl);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_gl);
        glMaterialf(GL_FRONT, GL_SHININESS, highlight_gl);

    @staticmethod
    def obsidianMaterial():
        """Change ambient, diffuse, specular and highlight components of light
            to mimic obsidian
        """
        ambient = [0.054, 0.05, 0.066, 1.0]
        ambient_gl = (GLfloat * len(ambient))(*ambient)

        diffuse = [0.18, 0.17, 0.23, 1.0]
        diffuse_gl = (GLfloat * len(diffuse))(*diffuse)

        specular = [0.33, 0.33, 0.35, 1.0]
        specular_gl = (GLfloat * len(specular))(*specular)

        highlight = 0.3*128
        highlight_gl = GLfloat(highlight)

        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_gl);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_gl);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_gl);
        glMaterialf(GL_FRONT, GL_SHININESS, highlight_gl);

    @staticmethod
    def goldMaterial():
        """Change ambient, diffuse, specular and highlight components of light
            to mimic gold
        """
        ambient = [0.25, 0.20, 0.07, 1.0]
        ambient_gl = (GLfloat * len(ambient))(*ambient)

        diffuse = [0.75, 0.61, 0.23, 1.0]
        diffuse_gl = (GLfloat * len(diffuse))(*diffuse)

        specular = [0.63, 0.56, 0.37, 1.0]
        specular_gl = (GLfloat * len(specular))(*specular)

        highlight = 0.4*128
        highlight_gl = GLfloat(highlight)

        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_gl);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_gl);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_gl);
        glMaterialf(GL_FRONT, GL_SHININESS, highlight_gl);

    @staticmethod
    def defaultMaterial():
        """Change ambient, diffuse, specular and highlight components of light
            back to defaults
        """
        ambient = [0.2, 0.2, 0.2, 1.0]
        ambient_gl = (GLfloat * len(ambient))(*ambient)

        diffuse = [0.8, 0.8, 0.8, 1.0]
        diffuse_gl = (GLfloat * len(diffuse))(*diffuse)

        specular = [0.0, 0.0, 0.0, 1.0]
        specular_gl = (GLfloat * len(specular))(*specular)

        highlight = 0.0*128
        highlight_gl = GLfloat(highlight)

        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_gl);
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_gl);
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular_gl);
        glMaterialf(GL_FRONT, GL_SHININESS, highlight_gl);