from pyglet import clock
import pyg3D.VectorFunctions as VectorFunctions

class AnimationManager:
    """ A system which performs a variety of animations on Object3D objects
        It handles frame by frame changes, allowing high level methods to
        be used to create animations.
    """

    def update(self,dt):
        """Iterate through the array of animations to perform each frame
        Animation methods are called with the dt parameter for their own
        calculations.

        :Parameter:
             'dt' : Int
                The time in seconds since the method was last called.
        """
        if len(self.animationMethods) >0:
            methodArrToUse = []
            for methodarr in reversed(self.animationMethods):
                if len(methodarr) > 0:
                    methodArrToUse = methodarr
                    continue
            for method in methodArrToUse:
                method(dt)


    def __init__(self, object):
        """Initialises with Object3D instance to animate and
        schedule update method
        :Parameter:
            'object' : Object3D
                    The object to be animated by this instance of
                    the animation manager
        """
        self.object = object
        self.animationMethods = []
        clock.schedule(self.update)

    def moveObject(self, vector, speed, time, enqueue = True):
        """Animate the movement of an object in a given direction
        at a given speed, for a given time.
        Adds method to array of methods to be called each frame to perform position changes

        :Parameters:
            'vector' : (float, float, float)
                The 3D vector expressing the direction to move the object.
            'speed' : float
                The speed at which to move the object.
            'time' : float
                The time in seconds to animate the object over.
            'enqueue' : bool
                Whether or not to perform the animation immediately or
                add it to the queue of animations to perform.

        """

        def movingAnimation(dt):
            movingAnimation.movementTime = movingAnimation.movementTime - dt
            distance = movingAnimation.movementSpeed*dt
            normalisedVector = VectorFunctions.normalise(movingAnimation.movementVector)
            self.object.position = (self.object.position[0] + normalisedVector[0]*distance, self.object.position[1] + normalisedVector[1]*distance, self.object.position[2] + normalisedVector[2]*distance)
            if (movingAnimation.movementTime <= 0):
                for animationArr in self.animationMethods:
                    if movingAnimation in animationArr:
                        animationArr.remove(movingAnimation)

        movingAnimation.movementVector = vector
        movingAnimation.movementSpeed = speed
        movingAnimation.movementTime = time
        if enqueue == True:
            self.animationMethods.append([movingAnimation])
        else:
            if len(self.animationMethods) == 0:
                self.animationMethods.append([])
            self.animationMethods[-1].append(movingAnimation)

    def scaleObject(self, amount, time, enqueue = True):
        """ Animates objects scale to a different value over a period of time
        Adds a scale method to array of methods to be called each frame to
        perform scale changes

        :Parameters:
            'amount' : (float,float,float)
                New scale along x, y and z axis for object
            'time' : float
                Time in seconds to perform
            'enqueue' : bool
                Whether or not to perform the animation immediately or
                add it to the queue of animations to perform.
        """

        def scalingAnimation(dt):
            scaleForTickFraction = float(dt) / scalingAnimation.scaleTime
            scalingAnimation.scaleTime = scalingAnimation.scaleTime - dt

            scaleValueForTick = (scaleForTickFraction * scalingAnimation.scaleDifference[0], scaleForTickFraction * scalingAnimation.scaleDifference[1],
                             scaleForTickFraction * scalingAnimation.scaleDifference[2])
            self.object.scale = (self.object.scale[0] + scaleValueForTick[0],self.object.scale[1] + scaleValueForTick[1],self.object.scale[2] + scaleValueForTick[2])

            scalingAnimation.scaleDifference = (
            scalingAnimation.scaleAmount[0] - self.object.scale[0], scalingAnimation.scaleAmount[1] - self.object.scale[1],
            scalingAnimation.scaleAmount[2] - self.object.scale[2])
            if(scalingAnimation.scaleTime <= 0):
                for animationArr in self.animationMethods:
                    if scalingAnimation in animationArr:
                        animationArr.remove(scalingAnimation)
                pass

        scalingAnimation.scaleAmount = amount
        scalingAnimation.scaleTime = time
        scalingAnimation.scaleDifference = (scalingAnimation.scaleAmount[0] - self.object.scale[0], scalingAnimation.scaleAmount[1] - self.object.scale[1],
                                            scalingAnimation.scaleAmount[2] - self.object.scale[2])
        if enqueue == True:
            self.animationMethods.append([scalingAnimation])
        else:
            if len(self.animationMethods) == 0:
                self.animationMethods.append([])
            self.animationMethods[-1].append(scalingAnimation)

    def rotateObject(self, angle,axis, time, enqueue = True):
        """Rotate object to a rotation angle over a period of time
            Adds method to array of methods to be called each frame to perform rotation changes

            :Parameters:
                'angle' : float
                    New angle to animate the object rotating to.
                'axis' : (float,float,float)
                    The axis to rotate the object around.
                'time' : float
                    The time in seconds to animate the objects rotation over.
        """

        def rotationAnimation(dt):
            rotationForTickFraction = float(dt) / rotationAnimation.rotationTime
            rotationAnimation.rotationTime = rotationAnimation.rotationTime - dt

            rotationValueForTick = rotationForTickFraction * rotationAnimation.rotationDifference
            self.object.rotation = [(self.object.rotation[0] + rotationValueForTick), axis[0],axis[1],axis[2]]

            rotationAnimation.rotationDifference = rotationAnimation.rotationAmount - self.object.rotation[0]
            if(rotationAnimation.rotationTime <= 0):
                for animationArr in self.animationMethods:
                    if rotationAnimation in animationArr:
                        animationArr.remove(rotationAnimation)
                pass

        rotationAnimation.rotationAmount = angle
        rotationAnimation.rotationTime = time
        rotationAnimation.rotationDifference = rotationAnimation.rotationAmount - self.object.rotation[0]
        if enqueue == True:
            self.animationMethods.append([rotationAnimation])
        else:
            if len(self.animationMethods) == 0:
                self.animationMethods.append([])
            self.animationMethods[-1].append(rotationAnimation)


