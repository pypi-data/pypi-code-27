import numpy as np
from pyglet.gl import *
from pyg3D import *
import pyg3D.VectorFunctions as VectorFunctions
from pyglet import *
class Camera:
    """ A class which allows the modification of a number of camera
    parameters. In addition to this, the class manages a variety of
    camera animations.

    """
    position = np.array([0,0,5])
    lookAt = np.array([0,0,0])
    upDir = np.array([0,1,0])
    width = 0
    height = 0
    fovy = 60.0
    near = 0.1
    far = 100.0
    target = None
    animationManagerInstance = None
    animationMethods = []

    @classmethod
    def update(cls,dt):
        """Iterate through array of animations to perform each frame

        :Parameter:
            'dt' : Int
                Time in seconds since the method was last called

        """
        if len(Camera.animationMethods) >0:
            methodArrToUse = []
            for methodarr in reversed(Camera.animationMethods):
                if len(methodarr) > 0:
                    methodArrToUse = methodarr
                    continue
            for method in methodArrToUse:
                method(dt)

    @classmethod
    def checkAnimationManagerInstance(cls):
        """ Ensures that the Camera classes animation manager instance is instantiated
        and that the update method has been scheduled for animations
        """
        if Camera.animationManagerInstance == None:
            Camera.animationManagerInstance = AnimationManager(Camera)
            clock.schedule(Camera.update)

    @classmethod
    def setTarget(cls, target):
        """ A method to set the cameras target.
        Changes the cameras current look at and target parameters.

        :Parameter:
            'target' : Object3D
                An Object3D object for the camera to target.
        """
        Camera.lookAt = target.position
        Camera.target = target


    @classmethod
    def animateFovTo(cls, fov, seconds, enqueue = True):
        """ Animates the camera's fov to a new value over a set amount
        of time.

        :Parameters:
            'fov' : float
                The new fov angle for the camera to be animated
                to.
            'seconds' : float
                The time in seconds for the animation to be performed.
            'enqueue' : bool
                Whether or not to perform the animation immediately or
                add it to the queue of animations to perform.
        """
        Camera.checkAnimationManagerInstance()
        def fovAnimation(dt):
            fovForTickFraction = float(dt) / fovAnimation.fovTime
            fovAnimation.fovTime = fovAnimation.fovTime - dt

            rotationValueForTick = fovForTickFraction * fovAnimation.fovDifference
            Camera.fovy = Camera.fovy + rotationValueForTick

            fovAnimation.fovDifference = fovAnimation.fovAmount - Camera.fovy
            if(fovAnimation.fovTime <= 0):
                for animationArr in Camera.animationMethods:
                    if fovAnimation in animationArr:
                        animationArr.remove(fovAnimation)
                pass

        fovAnimation.fovAmount = fov
        fovAnimation.fovTime = seconds
        fovAnimation.fovDifference = fovAnimation.fovAmount - Camera.fovy
        if enqueue == True:
            Camera.animationMethods.append([fovAnimation])
        else:
            if len(Camera.animationMethods) == 0:
                Camera.animationMethods.append([])
            Camera.animationMethods[-1].append(fovAnimation)

    @classmethod
    def moveCameraInDirection(cls, vector, speed, time, enqueue = True):
        """ Animates movement of the camera in a given direction at
         a given speed, over a given time.

        :Parameters:
            'vector' : (float, float, float)
                The 3D vector expressing the direction to move the camera.
            'speed' : float
                The speed at which to move the camera.
            'time' : float
                The time in seconds to animate the cameras movement over.
            'enqueue' : bool
                Whether or not to perform the animation immediately or
                add it to the queue of animations to perform.
        """
        Camera.checkAnimationManagerInstance()
        def movingAnimation(dt):
            movingAnimation.movementTime = movingAnimation.movementTime - dt
            distance = movingAnimation.movementSpeed*dt
            normalisedVector = VectorFunctions.normalise(movingAnimation.movementVector)
            Camera.position = (Camera.position[0] + normalisedVector[0]*distance, Camera.position[1] + normalisedVector[1]*distance, Camera.position[2] + normalisedVector[2]*distance)
            if (movingAnimation.movementTime <= 0):
                for animationArr in Camera.animationMethods:
                    if movingAnimation in animationArr:
                        animationArr.remove(movingAnimation)

        movingAnimation.movementVector = vector
        movingAnimation.movementSpeed = speed
        movingAnimation.movementTime = time
        if enqueue == True:
            Camera.animationMethods.append([movingAnimation])
        else:
            if len(Camera.animationMethods) == 0:
                Camera.animationMethods.append([])
            Camera.animationMethods[-1].append(movingAnimation)


    @classmethod
    def moveCameraToPosition(cls, position, time, enqueue = True):
        """ Animates the movement of the camera to a given position
        over a given amount of time.

        This method changes the eye position used in ``gluLookAt()``.

        :Parameters:
            'position' : (float,float,float)
                The position to animate the movement of the camera
                to.
            'time' : float
                The time in seconds to animate the cameras movement
                over.
            'enqueue' : bool
                Whether or not to perform the animation immediately or
                add it to the queue of animations to perform.

        """
        Camera.checkAnimationManagerInstance()

        def movingAnimation(dt):
            movingAnimation.movementTime = movingAnimation.movementTime - dt
            distance = ((Camera.position - np.array(position)) / movingAnimation.movementTime) * dt
            Camera.position = (Camera.position[0] - distance[0], Camera.position[1] - distance[1], Camera.position[2] - distance[2])
            if (movingAnimation.movementTime <= 0):
                for animationArr in Camera.animationMethods:
                    if movingAnimation in animationArr:
                        animationArr.remove(movingAnimation)

        movingAnimation.movementTime = time

        if enqueue == True:
            Camera.animationMethods.append([movingAnimation])
        else:
            if len(Camera.animationMethods) == 0:
                Camera.animationMethods.append([])
            Camera.animationMethods[-1].append(movingAnimation)

    @classmethod
    def moveLookAtInDirection(cls, vector, speed, time, enqueue = True):
        """ Animate a change in the look at position of the camera in
        a given direction at a given speed over a given time.

            :Parameters:
                'vector' : (float, float, float)
                    The 3D vector expressing the direction to move this point.
                'speed' : float
                    The speed at which to move it.
                'time' : float
                    The time in seconds to move the look at position over.
                'enqueue' : bool
                    Whether or not to perform the animation immediately or
                    add it to the queue of animations to perform.

        """
        Camera.checkAnimationManagerInstance()
        def movingAnimation(dt):
            movingAnimation.movementTime = movingAnimation.movementTime - dt
            distance = movingAnimation.movementSpeed*dt
            normalisedVector = VectorFunctions.normalise(movingAnimation.movementVector)
            Camera.lookAt = (Camera.lookAt[0] + normalisedVector[0]*distance, Camera.lookAt[1] + normalisedVector[1]*distance, Camera.lookAt[2] + normalisedVector[2]*distance)
            if (movingAnimation.movementTime <= 0):
                for animationArr in Camera.animationMethods:
                    if movingAnimation in animationArr:
                        animationArr.remove(movingAnimation)

        movingAnimation.movementVector = vector
        movingAnimation.movementSpeed = speed
        movingAnimation.movementTime = time
        if enqueue == True:
            Camera.animationMethods.append([movingAnimation])
        else:
            if len(Camera.animationMethods) == 0:
                Camera.animationMethods.append([])
            Camera.animationMethods[-1].append(movingAnimation)

    @classmethod
    def animateTargetChange(cls, newTarget, overTime, enqueue = True):
        """ Animate a change in the cameras current target, to a new
        one.

            :Parameters:
                'newTarget' : Object3D
                    The new target for the camera to transition to
                'overTime' : float
                    The time in seconds for the target change animation
                    to take place over.
                'enqueue' : bool
                    Whether or not to perform the animation immediately or
                    add it to the queue of animations to perform.
        """
        if Camera.target == None:
            raise TypeError("Camera has no current target to animate a change of target from")
            return

        Camera.checkAnimationManagerInstance()

        def cameraTargetChangeAnimation(dt):
            cameraTargetChangeAnimation.movementTime = cameraTargetChangeAnimation.movementTime - dt

            if not hasattr(cameraTargetChangeAnimation, "oldTarget"):
                cameraTargetChangeAnimation.oldTarget = Camera.target
                Camera.target = None

            distance = ((cameraTargetChangeAnimation.oldTarget.position - np.array(cameraTargetChangeAnimation.newTarget.position)) / overTime) * dt
            Camera.lookAt = (Camera.lookAt[0] - distance[0], Camera.lookAt[1] - distance[1], Camera.lookAt[2] - distance[2])
            if (cameraTargetChangeAnimation.movementTime <= 0):
                for animationArr in Camera.animationMethods:
                    if cameraTargetChangeAnimation in animationArr:
                        Camera.target = newTarget
                        animationArr.remove(cameraTargetChangeAnimation)

        cameraTargetChangeAnimation.movementTime = overTime
        cameraTargetChangeAnimation.newTarget = newTarget
        cameraTargetChangeAnimation.distance = ((Camera.lookAt - np.array(cameraTargetChangeAnimation.newTarget.position)) / overTime)

        if enqueue == True:
            Camera.animationMethods.append([cameraTargetChangeAnimation])
        else:
            if len(Camera.animationMethods) == 0:
                Camera.animationMethods.append([])
            Camera.animationMethods[-1].append(cameraTargetChangeAnimation)


