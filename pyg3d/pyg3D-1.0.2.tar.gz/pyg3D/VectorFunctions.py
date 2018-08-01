import math
import numpy as np

def normalise(vector):
    """Normalises a vector

    :Parameter:
        'vector' : (float,float,float)
            The vector to be normalised
    :rtype: [float,float,float]
    """

    result = []
    sumlistSquared = sum([item * item for item in vector])

    if abs(1 - sumlistSquared) < np.finfo(np.double).tiny:
        return vector
    magnitude = math.sqrt(sumlistSquared)
    if magnitude == 0:
        return [0,0,0]
    result.append(vector[0] / magnitude)
    result.append(vector[1] / magnitude)
    result.append(vector[2] / magnitude)
    return result