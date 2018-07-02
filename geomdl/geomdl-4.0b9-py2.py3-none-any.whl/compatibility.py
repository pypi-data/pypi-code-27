"""
.. module:: compatibility
    :platform: Unix, Windows
    :synopsis: Contains compatibility functions for CAD interoperability

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""


def change_ctrlpts_row_order(ctrlpts, size_u, size_v):
    """ Converts a u-row order 1-D control points list to a v-row order one.

    :param ctrlpts: control points in u-row order
    :type ctrlpts: list, tuple
    :param size_u: size in U-direction
    :type size_u: int
    :param size_v: size in V-direction
    :type size_v: int
    :return: control points in v-row order
    :rtype: list
    """
    new_ctrlpts = []
    for i in range(0, size_u):
        for j in range(0, size_v):
            temp = [float(c) for c in ctrlpts[i + (j * size_u)]]
            new_ctrlpts.append(temp)

    return new_ctrlpts


def flip_ctrlpts(ctrlpts, size_u, size_v):
    """ Flips a list of surface 1-D control points in v-row order.

    :param ctrlpts: control points
    :type ctrlpts: list, tuple
    :param size_u: size in U-direction (row length)
    :type size_u: int
    :param size_v: size in V-direction (column length)
    :type size_v: int
    :return: flipped control points
    :rtype: list
    """
    ctrlpts2d = []
    for i in range(0, size_u):
        ctrlpts_v = []
        for j in range(0, size_v):
            ctrlpts_v.append(ctrlpts[j + (i * size_v)])
        ctrlpts2d.append(ctrlpts_v)

    new_ctrlpts2d = flip_ctrlpts2d(ctrlpts2d, size_u, size_v)

    new_ctrlpts = []
    for i in range(0, size_v):
        for j in range(0, size_u):
            new_ctrlpts.append(new_ctrlpts2d[i][j])

    return new_ctrlpts


def flip_ctrlpts2d(ctrlpts2d, size_u=0, size_v=0):
    """ Flips a list of surface 2-D control points in *[u][v]* order.

    The resulting control points list will be in *[v][u]* order.

    :param ctrlpts2d: 2-D control points
    :type ctrlpts2d: list, tuple
    :param size_u: size in U-direction (row length)
    :type size_u: int
    :param size_v: size in V-direction (column length)
    :type size_v: int
    :return: flipped 2-D control points
    :rtype: list
    """
    if size_u <= 0 or size_v <= 0:
        # Detect array shapes
        size_u = len(ctrlpts2d)
        size_v = len(ctrlpts2d[0])

    new_ctrlpts2d = [[None for _ in range(size_u)] for _ in range(size_v)]
    for i in range(size_v):
        for j in range(size_u):
            new_ctrlpts2d[i][j] = [float(c) for c in ctrlpts2d[j][i]]

    return new_ctrlpts2d


# Reads 2D control points file, flips it and saves it
def flip_ctrlpts2d_file(file_in='', file_out='ctrlpts_flip.txt'):
    """ Flips u and v directions of a 2D control points file and saves flipped coordinates to a file.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Flip control points array
    new_ctrlpts2d = flip_ctrlpts2d(ctrlpts2d, size_u, size_v)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def generate_ctrlptsw(ctrlpts):
    """ Generates weighted control points from unweighted ones in 1-D.

    This function

    #. Takes in a 1-D control points list whose coordinates are organized in (x, y, z, w) format
    #. converts into (x*w, y*w, z*w, w) format
    #. Returns the result

    :param ctrlpts: 1-D control points (P)
    :type ctrlpts: list
    :return: 1-D weighted control points (Pw)
    :rtype: list
    """
    # Multiply control points by weight
    new_ctrlpts = []
    for cpt in ctrlpts:
        temp = [float(pt * cpt[-1]) for pt in cpt]
        temp[-1] = float(cpt[-1])
        new_ctrlpts.append(temp)

    return new_ctrlpts


def generate_ctrlptsw2d(ctrlpts2d):
    """ Generates weighted control points from unweighted ones in 2-D.

    This function

    #. Takes in a 2D control points list whose coordinates are organized in (x, y, z, w) format
    #. converts into (x*w, y*w, z*w, w) format
    #. Returns the result

    Therefore, the returned list could be a direct input of the NURBS.Surface class.

    :param ctrlpts2d: 2-D control points (P)
    :type ctrlpts2d: list
    :return: 2-D weighted control points (Pw)
    :rtype: list
    """
    # Multiply control points by weight
    new_ctrlpts2d = []
    for row in ctrlpts2d:
        ctrlptsw_v = []
        for col in row:
            temp = [float(c * col[-1]) for c in col]
            temp[-1] = float(col[-1])
            ctrlptsw_v.append(temp)
        new_ctrlpts2d.append(ctrlptsw_v)

    return new_ctrlpts2d


# Generates weighted control points from unweighted ones
def generate_ctrlptsw2d_file(file_in='', file_out='ctrlptsw.txt'):
    """ Generates weighted control points from unweighted ones in 2-D.

    This function

    #. Takes in a 2-D control points file whose coordinates are organized in (x, y, z, w) format
    #. Converts into (x*w, y*w, z*w, w) format
    #. Saves the result to a file

    Therefore, the resultant file could be a direct input of the NURBS.Surface class.

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Multiply control points by weight
    new_ctrlpts2d = generate_ctrlptsw2d(ctrlpts2d)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def generate_ctrlpts_weights(ctrlpts):
    """ Generates unweighted control points from weighted ones in 1-D.

    This function

    #. Takes in 1-D control points list whose coordinates are organized in (x*w, y*w, z*w, w) format
    #. Converts the input control points list into (x, y, z, w) format
    #. Returns the result

    :param ctrlpts: 1-D control points (P)
    :type ctrlpts: list
    :return: 1-D weighted control points (Pw)
    :rtype: list
    """
    # Divide control points by weight
    new_ctrlpts = []
    for cpt in ctrlpts:
        temp = [float(pt / cpt[-1]) for pt in cpt]
        temp[-1] = float(cpt[-1])
        new_ctrlpts.append(temp)

    return new_ctrlpts


def generate_ctrlpts2d_weights(ctrlpts2d):
    """ Generates unweighted control points from weighted ones in 2-D.

    This function

    #. Takes in 2-D control points list whose coordinates are organized like (x*w, y*w, z*w, w)
    #. Converts the input control points list into (x, y, z, w) format
    #. Returns the result

    :param ctrlpts2d: 2-D control points (P)
    :type ctrlpts2d: list
    :return: 2-D weighted control points (Pw)
    :rtype: list
    """
    # Divide control points by weight
    new_ctrlpts2d = []
    for row in ctrlpts2d:
        ctrlptsw_v = []
        for col in row:
            temp = [float(c / col[-1]) for c in col]
            temp[-1] = float(col[-1])
            ctrlptsw_v.append(temp)
        new_ctrlpts2d.append(ctrlptsw_v)

    return new_ctrlpts2d


# Generates unweighted control points from weighted ones
def generate_ctrlpts2d_weights_file(file_in='', file_out='ctrlpts_weights.txt'):
    """ Generates unweighted control points from weighted ones in 2-D.

    #. Takes in 2-D control points list whose coordinates are organized like (x*w, y*w, z*w, w)
    #. Converts the input control points list into (x, y, z, w) format
    #. Saves the result to a file

    :param file_in: name of the input file (to be read)
    :type file_in: str
    :param file_out: name of the output file (to be saved)
    :type file_out: str
    """
    # Read control points
    ctrlpts2d, size_u, size_v = _read_ctrltps2d_file(file_in)

    # Divide control points by weight
    new_ctrlpts2d = generate_ctrlpts2d_weights(ctrlpts2d)

    # Save new control points
    _save_ctrlpts2d_file(new_ctrlpts2d, size_u, size_v, file_out)


def combine_ctrlpts_weights(ctrlpts, weights=None):
    """ Multiplies control points by the weights to generate weighted control points.

    This function is dimension agnostic, i.e. control points can be in any dimension but weights should be 1D.

    The ``weights`` function parameter can be set to None to let the function generate a weights vector composed of
    1.0 values. This feature can be used to convert B-Spline basis to NURBS basis.

    :param ctrlpts: unweighted control points
    :type ctrlpts: list, tuple
    :param weights: weights vector; if set to None, a weights vector of 1.0s will be automatically generated
    :type weights: list, tuple or None
    :return: weighted control points
    :rtype: list
    """
    if weights is None:
        weights = [1.0 for _ in range(len(ctrlpts))]

    ctrlptsw = []
    for pt, w in zip(ctrlpts, weights):
        temp = [float(c * w) for c in pt]
        temp.append(float(w))
        ctrlptsw.append(temp)

    return ctrlptsw


def separate_ctrlpts_weights(ctrlptsw):
    """ Divides weighted control points by weights to generate unweighted control points and weights vector.

    This function is dimension agnostic, i.e. control points can be in any dimension but the last element of the array
    should indicate the weight.

    :param ctrlptsw: weighted control points
    :type ctrlptsw: list, tuple
    :return: unweighted control points and weights vector
    :rtype: list
    """
    ctrlpts = []
    weights = []
    for ptw in ctrlptsw:
        temp = [float(pw / ptw[-1]) for pw in ptw[:-1]]
        ctrlpts.append(temp)
        weights.append(ptw[-1])

    return [ctrlpts, weights]


def _read_ctrltps2d_file(file_in):
    ctrlpts = []
    size_u = 0
    size_v = 0

    try:
        with open(file_in, 'r') as fp:
            for line in fp:
                line = line.strip()
                control_point_row = line.split(';')
                size_v = 0
                ctrlpts_v = []
                for cpr in control_point_row:
                    cpt = cpr.split(',')
                    pt_temp = []
                    for pt in cpt:
                        pt_temp.append(float(pt.strip()))
                    ctrlpts_v.append(pt_temp)
                    size_v += 1
                ctrlpts.append(ctrlpts_v)
                size_u += 1
    except IOError:
        raise ValueError("File " + str(file_in) + " cannot be opened for reading")

    return ctrlpts, size_u, size_v


def _save_ctrlpts2d_file(ctrlpts2d, size_u, size_v, file_out):
    try:
        with open(file_out, 'w') as fp:
            fp.truncate()
            for i in range(size_u):
                line = ""
                for j in range(size_v):
                    for idx, coord in enumerate(ctrlpts2d[i][j]):
                        if idx:  # Add comma if we are not on the first element
                            line += ","
                        line += str(coord)
                    if j != size_u - 1:
                        line += ";"
                    else:
                        line += "\n"
                fp.write(line)
    except IOError:
        raise ValueError("File " + str(file_out) + " cannot be opened for writing")
