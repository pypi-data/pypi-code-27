# -*- coding: utf-8 -*-

import collections
import functools
import itertools
import json
import logging
import sys

import svgwrite

from . import check
from . import core
from . import drawTemplate as svg


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# helper functions

def _load_matrix_from_input(fp):
    """
    Load a linking matrix from a JSON file.

    Deserialize `fp` (a `.read()`-supporting text file containing a JSON
    document) to a Python object compatible with the structure of a linking
    matrix.

    A linking matrix serialized as a JSON document must be structured as a JSON
    array made of arrays of integers.  The validity of the matrix is not
    checked by this function.

    If the data being deserialized has not a structure compatible with the
    structure of a linking matrix, a TypeError will be raised.
    """

    # interpret the input as a JSON file
    try:
        matrix = json.load(fp)
    except json.JSONDecodeError as err:
        raise TypeError('Malformed JSON') from err

    # check the loaded input JSON structure is compatible with a linking matrix
    # object: i.e., a List[List[int]]
    if not isinstance(matrix, list):
        raise TypeError('Invalid input structure')
    if not matrix:  # empty linking matrix
        raise TypeError('Invalid input structure')
    for row in matrix:
        if not isinstance(row, list):
            raise TypeError('Invalid input structure')
        for coeff in row:
            if not isinstance(coeff, int):
                raise TypeError('Invalid input structure')

    return matrix


# optimization code, tree construction

def getPermutations(matrix):
    """return an iterator of all the crossings to perform"""
    size = len(matrix)
    for i in range(size):
        for j in range(i):
            # yield as many times as the strands cross
            yield from itertools.repeat((j, i), abs(matrix[i][j]))


def _pairwise(iterable):
    # see https://docs.python.org/3/library/itertools.html#itertools-recipes
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def getNeighbours(position):
    """return an iterator of the neighbour pairs"""
    for left, right in _pairwise(position):
        if left < right:
            yield left, right
        else:
            yield right, left


def detectDoubles(permutationlist):
    """check whether permutationList contains multiple crossings for the same strand"""
    already_permuted = set()
    for perm in permutationlist:
        for strand in perm:
            if strand in already_permuted:
                return True  # strand is permuted more than once: double
            else:
                already_permuted.add(strand)
    return False


def all_subsets(position):
    combinator = functools.partial(
        itertools.combinations,
        list(getNeighbours(position))
    )
    subsets = itertools.chain.from_iterable(
        map(
            combinator,
            reversed(range(1, len(position) // 2 + 1))  # give priority to subsets with many permutations
        )
    )
    return subsets


def updatePermutationList(permList, toRemove):
    out = list(permList)  # do not alter original, permList is a list of tuple
    for permutation in toRemove:
        out.remove(permutation)
    return out


def updatePosition(position, toPermute):
    out = list(position)  # do not alter original, position is a list of int
    for perm in toPermute:
        ind1 = position.index(perm[0])
        ind2 = position.index(perm[1])
        out[ind1], out[ind2] = out[ind2], out[ind1]
    return out


class Node:
    def __init__(self, permutationList, currentPosition, parent=None, depth=0, transition=None):
        self.currentPosition = currentPosition
        self.permutationList = permutationList
        self.incomingTransition = transition
        self.parent = parent
        self.children = []
        self.depth = depth

    def addChild(self, child):
        self.children.append(child)

    def getPossibleTransitions(self):
        transitions = []

        potential_transitions = itertools.filterfalse(
            detectDoubles,  # remove transitions permuting the same strand many times
            all_subsets(self.currentPosition)
        )
        for subset in potential_transitions:
            for perm in subset:
                if perm not in self.permutationList:
                    # perm is not a valid permutation: subset is not a valid
                    # transition
                    break
            else:
                # all permutations in subset are in self.permutionList: subset
                # is a valid transition
                transitions.append(subset)

        assert sorted(transitions, key=len, reverse=True) == transitions
        return transitions


class Tree:
    def __init__(self):
        self.structure = []
        self.leaf = None

    def addNode(self, node):
        self.structure.append(node)

    def getAtDepth(self, depth):
        if len(self.structure) == 0:
            return []
        atDepth = []
        for node in self.structure:
            if node.depth == depth:
                atDepth.append(node)
        return atDepth

    def getShortestPaths(self):
        if len(self.structure) == 0:
            return []
        endpoint = self.leaf
        path = [endpoint.incomingTransition]
        node = endpoint
        while node.parent != None:
            node = node.parent
            if node.incomingTransition != None:
                path.insert(0, node.incomingTransition)
        logger.info('Shortest template')
        for level, step in enumerate(path, start=1):
            logger.info(f'  Level {level}: {", ".join(map(str, sorted(step)))}')
        return path


def createTree(matrix):
    assert check.is_linking(matrix)
    tree = Tree()
    initialPosition = list(range(len(matrix)))
    permList = list(getPermutations(matrix))
    root = Node(permList, initialPosition)
    logger.info(f'Maximum possible template length: {len(permList)}')
    level = 0
    lifo = collections.deque()
    lifo.append((root, level))
    finalPosition = core.final_position(matrix)
    while lifo:
        head = lifo.popleft()
        if head[1] != level:
            logger.info(f'  Exploring depth {head[1]} of the permutation tree')
        node, level = head
        tree.addNode(node)
        for transition in node.getPossibleTransitions():
            child = Node(updatePermutationList(node.permutationList, transition),
                         updatePosition(node.currentPosition, transition), node, node.depth + 1, transition)
            node.addChild(child)
            lifo.append((child, level + 1))
            if len(child.permutationList) == 0 and finalPosition == child.currentPosition:
                tree.leaf = child
                return tree
    return tree


def getTorsions(matrix):
    return [matrix[i][i] for i in range(len(matrix))]


def drawSVGTemplate(matrix, tree, output, entireTemplate=False, white=False, scale=1.0):
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22",
              "#17becf", "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7",
              "#dbdb8d", "#9edae5"]
    dwg = svgwrite.Drawing()
    lengthTorsion = 40 * scale
    lengthPermut = 100 * scale
    try:
        shortestPath = tree.getShortestPaths()
    except AttributeError:
        shortestPath = []
    torsions = getTorsions(matrix)
    maxTorsions = abs(max(torsions, key=abs))
    coord = []
    start_height = 100 * scale
    if white:
        colors = ["white"] * 20
    if entireTemplate:
        start_height += len(matrix) * 100 * scale
    for i in range(len(matrix)):
        coord.append([(i * 100 * scale + start_height, start_height) for j in range(len(shortestPath)+maxTorsions+1)])
    for i in range(len(matrix)-1):
        svg.upperSemiCircle(coord[i][0][0] + 40 * scale, coord[i][0][1], coord[i+1][0][0], coord[i+1][0][1], dwg, scale)
    for i in range(1,maxTorsions+1):
        for j in range(len(coord)):
            coord[j][i] = (coord[j][i-1][0], coord[j][i-1][1]+lengthTorsion)
            #make torsion
            if torsions[j] == 0:
                svg.straightTransition(coord[j][i-1][0], coord[j][i-1][1], dwg, lengthTorsion, colors[j%20], scale)
            elif torsions[j] > 0 :
                svg.positiveTorsion(coord[j][i-1][0], coord[j][i-1][1], dwg, colors[j%20], scale)
                torsions[j] -= 1
            else:
                svg.negativeTorsion(coord[j][i-1][0], coord[j][i-1][1], dwg, colors[j%20], scale)
                torsions[j] += 1
    for i in range(maxTorsions+1, len(coord[0])):
        round = shortestPath[i - maxTorsions - 1]
        for transformation in round:
            coord[transformation[0]][i], coord[transformation[1]][i] = \
                (coord[transformation[1]][i-1][0],coord[transformation[1]][i-1][1]+lengthPermut), \
                (coord[transformation[0]][i-1][0],coord[transformation[0]][i-1][1]+lengthPermut)
            #make permut
            #positive permutation
            if matrix[transformation[0]][transformation[1]] > 0:
                if coord[transformation[0]][i-1][0] < coord[transformation[1]][i-1][0]:
                    svg.leftPermut(coord[transformation[0]][i-1][0], coord[transformation[0]][i-1][1],
                                   dwg, colors[transformation[0]%20], scale)
                    svg.rightPermut(coord[transformation[1]][i-1][0], coord[transformation[1]][i-1][1],
                                    dwg, colors[transformation[1]%20], scale)
                else :
                    svg.leftPermut(coord[transformation[1]][i-1][0], coord[transformation[1]][i-1][1],
                                   dwg, colors[transformation[1]%20], scale)
                    svg.rightPermut(coord[transformation[0]][i-1][0], coord[transformation[0]][i-1][1],
                                    dwg, colors[transformation[0]%20], scale)
            #negative permutation
            else :
                if coord[transformation[0]][i-1][0] < coord[transformation[1]][i-1][0]:
                    svg.rightPermut(coord[transformation[1]][i-1][0], coord[transformation[1]][i-1][1],
                                    dwg, colors[transformation[1]%20], scale)
                    svg.leftPermut(coord[transformation[0]][i-1][0], coord[transformation[0]][i-1][1],
                                   dwg,colors[transformation[0]%20], scale)
                else :
                    svg.rightPermut(coord[transformation[0]][i-1][0], coord[transformation[0]][i-1][1],
                                    dwg,colors[transformation[0]%20], scale)
                    svg.leftPermut(coord[transformation[1]][i-1][0], coord[transformation[1]][i-1][1],
                                   dwg,colors[transformation[1]%20], scale)
        for j in range(len(coord)):
            if coord[j][i] == coord[j][0]:
                coord[j][i] = (coord[j][i-1][0], coord[j][i-1][1]+lengthPermut)
                #draw straight line
                svg.straightTransition(coord[j][i-1][0], coord[j][i-1][1], dwg, lengthPermut, colors[j%20], scale)
    finalPosition = core.final_position(matrix)
    left_coord = ([coord[finalPosition[0]][-1][0], coord[finalPosition[0]][-1][1] + 100 * scale])
    right_coord = ([coord[finalPosition[-1]][-1][0] + 40 * scale, coord[finalPosition[-1]][-1][1] + 100 * scale])
    for position in finalPosition:
        svg.bottom(coord[position][-1][0], coord[position][-1][1], left_coord[0], left_coord[1], right_coord[0], right_coord[1],
                   dwg, colors[position%20], scale)
    x,y = coord[0][0][0], coord[0][0][1]
    x2,y2 = coord[-1][0][0] + 40 * scale, coord[-1][0][1]
    if not entireTemplate:
        top_left = (x, y)
        top_right = (x2, y2)
        svg.top(top_left[0], top_left[1], top_right[0], top_right[1], dwg, scale)
    else:
        x3,y3 = x - 80 * scale, y
        x4,y4 = x3 - (x2 - x), y
        x5,y5 = coord[finalPosition[0]][-1][0], coord[finalPosition[0]][-1][1] + 100 * scale
        x6,y6 = coord[finalPosition[-1]][-1][0] + 40 * scale, y5
        x7,y7 = x3, y5
        x8,y8 = x4, y5
        svg.upperSemiCircle(x3 + 1, y3, x, y, dwg, scale)
        svg.upperSemiCircle(x4 + 1, y4, x2 - 1, y2, dwg, scale)
        svg.lowerSemiCircle(x7 + 1, y7, x5, y5, dwg, scale)
        svg.lowerSemiCircle(x8 + 1, y8, x6 - 1, y6, dwg, scale)
        svg.straightLine(x3, y3, y5 - y, dwg, scale)
        svg.straightLine(x4, y4, y5 - y, dwg, scale)
    dwg.write(output)


###############################################################################

def run(infile, *, output, color=True, complete_flow=False, scale=1.0):

    try:
        if infile == '-':  # the special argument '-' means stdin
            matrix = _load_matrix_from_input(sys.stdin)
        else:
            with open(infile) as fp:
                matrix = _load_matrix_from_input(fp)
    except TypeError:
        logger.error("Invalid JSON input")
        exit(code=1)
    except OSError as err:
        logger.critical(f'Unable to read input: {err}')
        exit(code=2)

    if not check.is_linking(matrix):
        logger.error("No tree created due to invalid matrix")
        exit(code=1)

    logger.info('Input matrix')
    for m in matrix:
        logger.info(f'  {m}')

    logger.info("Starting constructing the tree")
    myTree = createTree(matrix)
    logger.info("Finished constructing the tree")

    logger.info("Starting creation of the SVG template")
    try:
        if output == '-':  # the special argument '-' means stdout
            drawSVGTemplate(matrix, myTree, sys.stdout, entireTemplate=complete_flow, white=not color, scale=scale)
        else:
            with open(output, mode='w') as fp:
                drawSVGTemplate(matrix, myTree, fp, entireTemplate=complete_flow, white=not color, scale=scale)
    except OSError as err:
        logger.critical(f'Unable to write output: {err}')
        exit(code=2)
    logger.info("Finished creation of the SVG template")
