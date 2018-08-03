# -*- coding: utf-8 -*-
"""
:date: 2018-07-30
:author: Luis Ulloa
:license: MIT-license

My implementation of a linear algebra library in Python. Consists of
a Vector and Matrix class that can be compatible with one another, as
well as useful methods for interacting with both concepts/classes.
"""

from math import gcd, pow, sqrt, isclose
from linear_lib.linear_tests import *
from fractions import Fraction


class Vector:
    """
    The Vector class imitates the m x 1 vector from linear algebra and
    contains many useful functions for dealing and interacting with Vectors.

    Getting values directly from the vector should be done using the get(index)
    function since the comp vector location in memory may change with functions
    like mag() or zero().

    class Vector
    __init__(comp)          - takes in a list of components or a valid mx1 Matrix
    resize(length)          - while preserving current elements or filling with 0's, changes current vector length
    set(comp, index=-1)     - sets entire list at once or one specific index/value
    get(index)              - returns item at specified index of vector
    zero()                  - turns the current vector into a zero vector and returns it
    mag()                   - returns the magnitude of current vector
    normalize(change=False) - returns normalized current vector, if change=True, internal vector is updated
    same_normalized(other)  - returns True/False depending on equality of the two vectors once normalized
    dot(other)              - returns the dot product of th two vectors
    cross(other)            - returns the cross product of u x v (u is current vector, v is other)
    perp(other)             - returns True/False if current and other are/aren't perpendicular
    parallel(other)         - returns True/False if current and other are/aren't parallel
    indep(other)          - returns True/False if curr vector and other vector(s) are linearly independent
    operator +              - returns sum of two vectors, component wise addition
    operator -              - returns difference of two vectors, component wise subtraction
    operator *              - alternate for dot product, or can use for vector scaling
    operator **             - returns original vector with its components raised to power
    operator ==             - checks to see if lists are equal
    to string method        - format: "<elem1, elem2, ...>"
    len() method            - can use len() to get vector length
    get and set []          - user can get and set values in vector with index based operations []

    comp = vector composition, list of components
    length = number of components in vector
    rows = same as length, used with cols for backwards compatibility with Matrix
    cols = 1 (num of columns)
    """

    def __init__(self, comp=[]):
        """
        Initializes the vector with either a list containing its components
        or an appropriate Matrix with mx1 dimensions. Defaults to an empty
        vector if not specified.

        :param comp: a list of the elements to be included in the vector;
                        the initial components, defaulted to an empty list.
                        could also be an appropriately sized Matrix
        :type comp: list, Matrix
        :return: none
        :raises: ValueError when Matrix is invalid size for Vector conversion
        """
        if isinstance(comp, Matrix):
            if comp.cols == 1:
                self.comp = [row[0] for row in comp.comp]
            else:
                raise ValueError("Cannot convert Matrix with greater than 1 column to Vector.")
        else:
            self.comp = comp             # user should never change comp directly; use set()

        self.length = len(self.comp)     # user should never change length directly; use resize()
        self.rows = self.length          # rows and cols included for backwards compatibility as
        self.cols = 1                    # a Matrix and for use in matrix-vector product

    def resize(self, length):
        """
        Re-sizes the vector to the specified length. If length is greater than
        current size, the new components are initialized with 0, otherwise if length
        is less than current size, the last few components are lost.

        :param length: new length of vector
        :type length: int
        :return: current vector, now resized
        :rtype: Vector
        """
        assert(length >= 0)                # no negative lengths
        dist = length - self.length

        if dist < 0:
            self.comp = self.comp[:dist]  # notice how this fails when dist = 0, but else correctly handles it
        else:
            self.comp = self.comp + [0]*dist

        self.length = length
        return self

    def set(self, comp, index=-1):
        """
        Set/change the values of the current vector. Can either pass in a new
        list to replace the internal list, or can specify an index in vector
        to change just that value, in which case comp can be a single value.
        No errors are thrown if user re-sizes the list.

        :param comp: list to replace whole vector or value to replace single component
        :param index: optional parameter that specifies the index of the value to be replaced
        :type comp: list, int, float
        :type index: int, float (that is whole ex. 1.0)
        :return: current vector, now updated
        :rtype: Vector
        :raises: index error if out of bounds index
        """
        if index < 0:                   # default None and index=0 calls would conflict
            self.comp = comp
            self.length = self.rows = len(comp)
        else:
            if index >= self.length:
                raise IndexError("Index out of bounds in vector.")
            self.comp[index] = comp
        return self

    def get(self, index):
        """
        :param index: index of value
        :type index: int
        :return: element at specified index
        :rtype: int, float
        :raises: IndexError if index not in vector
        """
        if 0 <= index < self.length:
            return self.comp[index]
        else:
            raise IndexError("Specified index is not in vector.")

    def zero(self):
        """
        Zeroes out the current vector by replacing each component with a 0.

        :return: returns current vector, which is now a zero vector
        :rtype: Vector
        """
        self.comp = [0]*self.length
        return self

    def mag(self):
        """
        Will get the magnitude of a vector.

        :return: the magnitude of a vector (sqrt(sum of components squared))
        :rtype: int, float
        """
        return sqrt(sum([pow(x, 2) for x in self.comp]))

    def normalize(self, change=False):
        """
        Normalizes a vector (acts on internal vector, does not take in a vector)

        :param change: if True, internal vector components are changed in addition
                          to returning vector
                 if False, vector says the same but normalized vector is returned;
                           default is false
        :type change: bool
        :return: another Vector but with the normalized components (False)
                 current Vector but with normalized components (True)
        :rtype: Vector
        """
        magnitude = self.mag()
        if magnitude == 0:      # already zero vector
            return self

        if change:
            self.comp = [elem / magnitude for elem in self.comp]
            return self
        else:
            return Vector([x / magnitude for x in self.comp])

    def same_normalized(self, other):
        """
        This function states whether the current vector is the same as other
        vector when normalized.

        :param other: other vector to be compared
        :type other: Vector
        :return: True if they have same normalized version, False otherwise
        :rtype: bool
        """
        return self.normalize() == other.normalize()

    def dot(self, other):
        """
        This function returns a scalar (number) value representing the dot
        product of the current vector and the other vector.

        :param other: the b vector in a dot b
        :type other: Vector
        :return: The dot product of the current vector and other vector.
        :rtype: int, float
        :raises: ValueError when vectors are not the same length
        """
        if len(self.comp) == len(other.comp):
            return sum([x * y for x, y in zip(self.comp, other.comp)])
        else:
            raise ValueError("Invalid vectors - must be of same length.")

    def cross(self, other):
        """
        For 3-dimensional vectors (3x1), this function allows you to take
        the cross product, which produces a vector i.e. orthogonal to both.

        :param other: 3D Vector (b in a X b)
        :return: Vector representing cross product of current and other
        :rtype: Vector
        :raises: Value error if vectors are not 3 dimensional
        """

        # Simplified version, after determinants: u is current vector v is other
        # u x v = (u2v3 - u3v2)i - (u1v3-u3v1)j + (u1v2-u2v1)k
        if self.length == 3 and other.length == 3:
            i_hat = self.comp[1]*other.comp[2] - self.comp[2]*other.comp[1]
            j_hat = -1 * (self.comp[0]*other.comp[2] - self.comp[2]*other.comp[0])
            k_hat = self.comp[0]*other.comp[1] - self.comp[1]*other.comp[0]
            return Vector([i_hat, j_hat, k_hat])
        else:
            raise ValueError("Invalid vectors - Can only take the cross product of 3D vectors.")

    def perp(self, other):
        """
        Boolean function for whether two vectors are perpendicular/orthogonal to each other.

        :param other: the other vector
        :type other: Vector
        :return: Will return True if current vector and other vector are perpendicular, false otherwise.
        :rtype: bool
        """

        return self.dot(other) == 0

    def parallel(self, other):
        """
        Boolean function for whether two vectors are parallel to each other.

        :param other: the other vector
        :type other: Vector
        :return: Will return True if current vector and other vector are parallel, false otherwise.
        :rtype: bool
        """

        return self.cross(other).mag() == 0   # could also check dot prod = |A*B|

    def indep(self, other):
        """
        Determines whether current vector and one or more vectors are linearly independent.

        Note: User should make sure to pass in vectors of correct dimension.

        :param other: list of vectors or a vector to be compared to current
        :type other: List, Vector
        :return: boolean true/false if given vectors are linearly independent
        :rtype: bool
        :raises: ValueError if other is not a valid type
        """

        if isinstance(other, Vector):   # make 'other' a list if it's a vector
            other = [other]

        if isinstance(other, list) and len(other) > 0:
            other.append(self)
            m, n = len(other), len(other[0])    # m is num vectors, n is vector dimension

            if m == n:              # Place list into matrix and check if determinant is 0
                return Matrix([vec.comp for vec in other]).det() != 0
            elif m < n:
                row_reduced = Matrix([vec.comp for vec in other]).row_reduce()
                return Vector(row_reduced[-1]).mag() != 0   # see if last row is all 0s
            else:
                return False    # if num vectors > dimension, can't be independent

        else:
            raise ValueError("Invalid input - Must be a vector or list of vectors.")

    def __add__(self, other):
        """
        Adding two vectors returns a vector with the respective components
        added together as expected. (does not affect this or other vector's
        components)

        :param other: the other vector to be added to current instance vector
        :type other: Vector
        :return: a vector with the resulting added components
        :rtype: Vector
        :raises: ValueError when vectors are not the same length
        """
        if len(self.comp) == len(other.comp):
            return Vector([x+y for x, y in zip(self.comp, other.comp)])
        else:
            raise ValueError("Invalid vectors - must be of same length.")

    def __sub__(self, other):
        """
       Subtracting two vectors returns a vector with the respective components
       subtracted. "current - other" is formatting. (this does not affect this
       or other vector's components)

       :param other: the other vector which is subtracting from the current vector
       :type other: Vector
       :return: a vector with the resulting subtracted components
       :rtype: Vector
       :raises: ValueError when vectors are not the same length
       """
        if len(self.comp) == len(other.comp):
            return Vector([x-y for x, y in zip(self.comp, other.comp)])
        else:
            raise ValueError("Invalid vectors - must be of same length.")

    def __mul__(self, other):
        """
        Multiplies the two vectors together; same functionality as calling the
        dot() function for dot product of current and other. Could also scale
        each component by a number

        :param other: the other vector
        :type other: Vector, integer, float
        :return: number value representing dot product of both vectors
        :rtype: int, float
        :raises: ValueError when vectors are not the same length
        """
        if isinstance(other, int) or isinstance(other, float):
            return Vector([x * other for x in self.comp])
        elif len(self.comp) == len(other.comp):
            return self.dot(other)
        else:
            raise ValueError("Invalid vectors - must be of same length.")

    def __eq__(self, other):
        """
        If two vectors have the same components, then they are equal. If the
        lists are not the same length, will always be False with no error thrown.

        :param other: other vector being tested for equality
        :type other: Vector
        :return: True or False based on equality
        :rtype: bool
        """
        return self.comp == other.comp  # compares lists

    def __pow__(self, power, modulo=None):
        """
        Allows you to raise each of the components of the current vector to a power.

        :param power: value to raise each component to
        :param modulo: optional parameter that applies the modulus operator to each result
        :type power: int, float
        :type modulo: int, float
        :return: a vector containing the appropriately scaled components
        :rtype: Vector
        """

        return Vector([pow(x, power) % modulo if modulo else pow(x, power) for x in self.comp])

    def __str__(self):
        """
        Converts vector to string by placing the components a, b , c, ... into arrow
        brackets, as such <a, b, c, ...>.  Empty arrays return <empty> for clarity.

        :return: a string detailing contents of vector with the format <a, b, c, ...> or <empty>
        :rtype: str
        """
        if self.length == 0:
            return "<empty>"
        vec = "<"
        for elem in self.comp:
            vec += str(elem) + ", "
        return vec[:-2] + ">"  # remove additional ", " and close

    def __len__(self):
        """
        :return: length of vector
        :rtype: int
        """
        return self.length

    def __getitem__(self, i):
        """
        Alternate for get(), allows you to reliably access components of vector.
        v = Vector([1,2]) v[0] -> 1

        :param i: index
        :type i: int
        :return: value at specified index in self.comp/vector
        :rtype: int, float
        """
        return self.get(i)

    def __setitem__(self, key, value):
        """
        Allows user to set value using index-based accessing.

        :param key:
        :param value:
        :return: item just inserted
        """
        return self.set(value, key)


class Matrix:
    """
    The Matrix class imitates the matrix concept from linear algebra and allows
    for different ways of dealing and interacting with matrices and vectors.

    class Matrix
    __init__(comp)          - takes in a list of components or a valid Vector
    resize(rows, cols)      - while preserving current elements or filling with 0's, changes current vector length
    set(comp, index=None)   - sets entire list at once or one specific index/value (tuple or array as (row, col))
    get(row=None,col=None)  - can get a specific row, column, or entire matrix composition (no args for matrix)
    zero()                  - replaces values in current matrix with all zeroes and returns it
    det()                   - takes the determinant of the current NxN matrix
    transpose()             - transposes the current mxn matrix to an nxm matrix (1st row becomes 1st col, etc.)
    row_echelon()           - returns the current matrix in row echelon form
    row_reduce()            - returns the current matrix to reduced row echelon form
    identity(n)             - static method that returns the nxn identity matrix
    combine(first, second)  - static method that combines two matrices by concatenation
    inverse()               - returns the inverse of current nxn matrix, or None if singular
    operator +              - returns sum of two matrices, component wise addition
    operator -              - returns difference of two matrices, component wise subtraction
    operator *              - matrix multiplication, matrix-vector product, scalar multiplication
    operator **             - returns original matrix with its components raised to power
    operator ==             - checks to see if internal lists are equal
    to string method        - format: "[row1\n row2\n row3\n ...]" and floats are shown as fractions
    len() method            - returns tuple formatted as (row, col)
    get and set [][]        - can get rows and specific values with [] or [][], and set specific values with [][]

    comp = matrix composition, list of lists where each list is a row
    rows = number of rows in matrix
    cols = number of columns in matrix
    """
    def __init__(self, comp=[]):
        """
        Initializes the matrix to the specified format. Default is an empty 0x0 matrix

        Note: It is up to the user to pass well-formed matrices, that is, two different
                rows cannot be different lengths, etc.

        :param comp: list of lists where each individual list represents a row,
                     similar to how numpy implements arrays; could also be a vector
        :type comp: list, Vector
        :return: none
        """

        if isinstance(comp, Vector):
            self.comp = [[row] for row in comp.comp]  # m x 1 Vector --> m rows
        else:
            self.comp = comp                          # list

        self.rows = len(self.comp)          # User should never be able to change instance
        if self.rows != 0:                  # variables directly, use an appropriate method
            self.cols = len(self.comp[0])
        else:
            self.cols = 0                   # if rows = 0, then no columns by default

    def resize(self, rows, cols):
        """
        Re-sizes the current matrix to the specified dimensions, rows x cols.
        Previous elements are left in place, if size is increased then new
        locations are filled with values of 0.

        :param rows: new row size
        :param cols: new column size
        :type rows: int, float
        :type cols: int, float
        :return: current matrix after resizing
        :rtype: Matrix
        """
        assert(rows >= 0 and cols >= 0)     # no negative dimensions allowed

        dist_rows = rows - self.rows
        dist_cols = cols - self.cols

        if dist_rows < 0:
            self.comp = self.comp[:dist_rows]
        else:
            for i in range(dist_rows):
                self.comp.append([0]*self.cols)  # update rows but don't have varying number of columns for each row

        if dist_cols < 0:                        # go through and shape columns now
            for i in range(rows):
                self.comp[i] = self.comp[i][:dist_cols]
        else:
            for i in range(rows):
                self.comp[i] += [0]*dist_cols

        self.rows = rows
        self.cols = cols
        return self

    def set(self, comp, index=None):
        """
        Set/change the current matrix. If index is not specified, then comp should
        be a list of lists detailing a new matrix. Otherwise, comp should be the
        integer value that goes in the specified index (row, column) tuple.

        :param comp: list of lists to replace matrix entirely, or single value
                     to replace a specific location in matrix
        :param index: optional tuple/list with (row, column) of value to be replaced
        :type comp: list of lists, int
        :type index: tuple, list
        :return: self, after edits are made
        :rtype: Matrix
        """

        if not index:
            assert(isinstance(comp, list))
            self.comp = comp
            self.rows = len(comp)
            if self.rows != 0:
                self.cols = len(comp[0])
            else:
                self.cols = 0
        else:
            assert(isinstance(comp, int))
            self.comp[index[0]][index[1]] = comp
        return self

    def get(self, row=None, col=None):
        """
        User can get rows, columns, the matrix comp list, or specific values
        in Matrix using this function and its optional parameters

        :param row: index of target row
        :param col: index of target col
        :type row: int
        :type col: int
        :return: element at specified row/col, or a row, or a col, or entire Matrix
        :rtype: int, list (row/col), List
        :raises: IndexError if row index or col index invalid
        """
        if row is not None and col is not None:  # value
            if 0 > row >= self.rows and 0 > col >= self.cols:
                raise IndexError("Row or column out of index bounds.")
            return self.comp[row][col]
        elif col is None and row is not None:    # row
            if 0 > row >= self.rows:
                raise IndexError("Row out of index bounds.")
            return self.comp[row]
        elif col is not None:                    # just col
            if 0 > col >= self.cols:
                raise IndexError("Col out of index bounds.")
            return [r[col] for r in self.comp]
        else:                                    # entire matrix
            return self.comp

    def zero(self):
        """
        Zeroes out the current matrix by replacing every element with a zero.

        :return: The current matrix, but updated to be the zero matrix.
        """
        self.comp = [[0]*self.cols for _ in range(self.rows)]
        return self

    def det(self):
        """
        Returns the determinant of an nxn matrix that is at least a 2x2. (recursive)

        :return: the determinant of the current matrix
        :rtype: int, float
        """

        if self.rows != self.cols:
            raise ValueError("Invalid matrix - only N x N matrices supported.")

        # base case -> 2 by 2
        if self.rows == 2 and self.cols == 2:  # ad - bc
            return self.comp[0][0] * self.comp[1][1] - self.comp[0][1] * self.comp[1][0]

        # going along top, along first row (not optimized to find best path)
        top_row = self.comp[0]
        determinant = 0
        for col_i in range(len(top_row)):
            # don't include in same row or column
            new_matrix = self.comp[1:]            # remove top row
            for r in range(len(new_matrix)):      # remove this column from each row
                new_matrix[r] = new_matrix[r][:col_i] + new_matrix[r][col_i + 1:]

            constant = top_row[col_i]
            if col_i % 2 == 1:
                constant *= -1  # every other constant is negative

            determinant += constant * Matrix(new_matrix).det()
        return determinant

    def transpose(self):
        """
        This function will return the transpose of the current matrix. (A -> A^T)
        "First row becomes first column, second row becomes second column, etc."

        :return: Transposed matrix
        :rtype: Matrix
        """
        return Matrix([[self.comp[r][c] for r in range(self.rows)] for c in range(self.cols)])

    @staticmethod
    def identity(n):
        """
        Static method for creating an identity matrix of dimension nxn.

        :param n: dimension of identity matrix
        :type n: int
        :return: identity matrix of size nxn
        :rtype: Matrix
        """
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    @staticmethod
    def combine(first, second):
        """
        Static method for concatenating two matrices, side by side.
        1 1   *combined  1  0    =      1 1 1 0
        2 2     with*    0  1    =      2 2 0 1

        Warning/Note: Matrices should have the same number of rows, otherwise
                        the minimum amount of rows will be present. (If first
                        has 3 rows and second has 5 rows, combined matrix has 3)

        :param first: first matrix
        :param second: second matrix
        :return: combined matrix, [[row1 + row2], ...]
        :rtype: Matrix
        """
        return Matrix([one + two for one, two in zip(first.comp, second.comp)])

    @staticmethod
    def _clean_matrix(new_matrix):
        """
        Not intended for client use. This method goes through matrix contents
        and reduces each row by the greatest common divisor of that row,
        multiplies row by -1 if leading pivot is negative, and turns floats
        into ints if no reduction occurs. self._clean_matrix or Matrix._clean_matrix

        :param new_matrix: matrix.comp, composition of matrix
        :type new_matrix: list
        :return: "cleaned" matrix comp
        :rtype: list
        """
        cols = len(new_matrix[0])
        for r, row in enumerate(new_matrix):
            gcf = row[0]
            for col in row[1:]:
                gcf = gcd(gcf, col)

            if gcf != 0:
                new_matrix[r] = row = [elem // gcf for elem in row]  # update row for next list comp

            c = 0
            while c < cols and row[c] == 0:
                c += 1
            if c < cols and row[c] < 0:
                new_matrix[r] = row = [-1*elem for elem in row]

            new_matrix[r] = [int(col) if int(col) == col else col for col in row]

        return new_matrix

    @staticmethod
    def _clear_pos(new_matrix, r, c, other_row):
        """
        Helper method for both row echelon functions.

        :param new_matrix: the matrix that will be updated by algorithmically
                            clearing one position in matrix
        :param r:  index of row to be changed
        :param c:   index of col to be changed
        :param other_row: index of other row being using in row operation
        :type r: int
        :type c: int
        :type other_row: list
        :return: matrix composition
        :rtype: list
        """
        above = new_matrix[r][c]
        const = new_matrix[other_row][c]  # row we will use

        # prioritize keeping numbers small / int division
        if const > above != 0 and const % above == 0:
            scale = const // above
            new_matrix[r] = [elem * scale for elem in new_matrix[r]]
        elif above >= const != 0 and const != 0 and above % const == 0:
            scale = above // const
            new_matrix[other_row] = [elem * scale for elem in new_matrix[other_row]]
        else:  # scale both
            new_matrix[r] = [elem * const for elem in new_matrix[r]]
            new_matrix[other_row] = [elem * above for elem in new_matrix[other_row]]
        new_matrix[r] = [curr - other for curr, other in
                         zip(new_matrix[r], new_matrix[other_row])]
        return new_matrix

    def row_echelon(self):
        """
        This function will row reduce the current matrix until it is in row echelon form.
        That is, until there is an upper triangular matrix. I've made a decent amount of
        optimizations in this function, but there definitely many others that could  be made.

        Note: This doesn't change the matrix internally, you will have to assign the
                return value to the your matrix variable if you want to change it.
              There is no guarantee that the matrix returned will contain only integers, may
                have floats.

        :return: row echelon form of current matrix
        :rtype: Matrix
        :return:
        """

        # adjust matrix so rows are in proper descending order / putting any pre-made pivots in place
        new_matrix = sorted(self.comp, reverse=True)
        start = 0   # by sorting, even if start is off, loop will be skipped and start will move ahead

        # store zero column indexes so we can adjust pivots later
        zero_cols = []
        for c in range(self.cols):
            if all(new_matrix[r][c] == 0 for r in range(self.rows)):
                zero_cols.append(c)

        r = curr_col = start                 # current row with pivot, current column with pivot
        while r < self.rows:                 # loop through each row after first
            for row_below_i in range(r+1, self.rows):    # enforce rows below have 0 in respective column r (rxr or cxc)
                while curr_col < self.rows and curr_col < self.cols and new_matrix[row_below_i][curr_col] != 0:
                    good_const_i = r     # row above/curr row won't mess with leading 0's
                    while new_matrix[good_const_i][curr_col] == 0:
                            good_const_i += 1

                    new_matrix = self._clear_pos(new_matrix, row_below_i, curr_col, good_const_i)

            # skip column from pivot consideration if it's a zero col
            curr_col += 1   # initial +1
            r += 1
            while curr_col in zero_cols:
                curr_col += 1

        new_matrix = self._clean_matrix(new_matrix)
        return Matrix(new_matrix)

    def row_reduce(self):
        """
        This function will row reduce the current matrix until it is in reduced row
        echelon form (RREF). The transpose of a matrix has the same RREF as original.

        Note: This doesn't change the matrix internally, you will have to assign the
                return value to the your matrix variable if you want to change it.

        :return: reduced row echelon form of current matrix
        :rtype: Matrix
        """

        new_matrix = self.row_echelon().comp     # get in row echelon form first

        pivots = {}     # store pivot indexes key-value for use later

        # store pivots as col : row pairs
        for r, row in enumerate(new_matrix):
            # identify pivot
            i = 0
            while i < self.cols and row[i] == 0:
                i += 1
            if i < self.cols:
                pivots[i] = r

        # apply only 0s above pivot (bottom part is done since already in row echelon form)
        offset = 0     # how far ahead the first pivot is (ex. may be zero cols before first pivot)
        for c in range(self.cols):
            if c in pivots:
                pivot_row = pivots[c]       # row the pivot is in
                for r in range(pivot_row):  # top part, don't loop past location of pivot
                    while new_matrix[r][c] != 0:    # stay in same column and fix parts above pivot
                        other_row = c-offset  # when no offset, col c can be cleared using row c since there are c zeros

                        new_matrix = self._clear_pos(new_matrix, r, c, other_row)
            else:
                offset += 1

        new_matrix = self._clean_matrix(new_matrix)  # this function also changes floats to perfect ints based on gcd

        # now, apply "each pivot is 1" rule, floats inevitable, but preserve as much ints as possible
        for r, row in enumerate(new_matrix):
            # identify pivot
            i = 0
            while i < self.cols and row[i] == 0:
                i += 1
            # divide row by proper amount to get a 1 on pivot
            if i < self.cols:
                pivot = row[i]
                new_matrix[r] = [elem // pivot if elem % pivot == 0 else elem / pivot for elem in row]
        return Matrix(new_matrix)

    def inverse(self):
        """
        Gets the inverse A^-1 of the current matrix A.

        :return: inverse matrix of current matrix, or None if not invertible (singular)
        :rtype: Matrix
        :raises: value error if current matrix is not nxn
        """
        n = self.cols
        identity = Matrix.identity(n)
        if self.rows != n:
            raise ValueError("Need an nxn matrix to calculate inverse.")
        # create combined matrix
        with_identity = Matrix.combine(self, identity).row_reduce()
        # if left side is identity, then right side is inverse
        if Matrix([row[:n] for row in with_identity.comp]) != identity:
            return None     # no inverse, singular
        else:
            return Matrix([row[-n:] for row in with_identity.comp])

    def __add__(self, other):
        """
        Adds two matrices and returns a matrix with the respective components
        added together as expected.

        :param other: the other matrix to be added to current instance matrix
        :type other: Matrix
        :return: a matrix with the resulting added components
        :rtype: Matrix
        :raises: ValueError when matrices do not have same dimensions
        """
        new_comp = []
        if self.rows == other.rows and self.cols == other.cols:
            for x, y in zip(self.comp, other.comp):
                new_comp.append([a + b for a, b in zip(x, y)])  # adding done in list comprehension
            return Matrix(new_comp)
        else:
            raise ValueError("Size mismatch, both matrices must have the same number of rows and columns.")

    def __sub__(self, other):
        """
       Subtracting two matrices returns a matrix with the respective components
       subtracted. "current - other" is formatting.

       :param other: the other matrix which is subtracting from the current matrix
       :type other: Matrix
       :return: a matrix with the resulting subtracted components
       :rtype: Matrix
       :raises: ValueError when matrices do not have same dimensions
       """
        new_comp = []
        if self.rows == other.rows and self.cols == other.cols:
            for x, y in zip(self.comp, other.comp):
                new_comp.append([a - b for a, b in zip(x, y)])  # subtracting done in list comprehension
            return Matrix(new_comp)
        else:
            raise ValueError("Size mismatch, both matrices must have the same number of rows and columns.")

    def __mul__(self, other):
        """
        Multiplies the two matrices together; aka Matrix Multiplication.
        Matrix-Vector product is also possible using the Vector class, though
        this method works for a mx1 matrix as well. Also configured to work with
        normal application of multiplying a scalar to a matrix.

        Notes: Approach is to take the dot product of each row of current matrix
                with each column of other matrix/vector. Since you typically write
                "Ax" where A is the matrix and x is the vector, this syntax should
                be adhered to when attempting matrix multiplication with these classes.

        :param other: the other matrix or vector, could also be an int or float for scaling
        :type other: Matrix, int, float
        :return: the resulting matrix
        :rtype: Matrix
        :raises: ValueError when there's a matrix multiplication size mismatch ([mxn]*[nxp]=[mxp])
        """
        new_matrix = []
        if isinstance(other, int) or isinstance(other, float):
            for row in self.comp:
                new_matrix.append([elem * other for elem in row])
            return Matrix(new_matrix)
        elif self.cols == other.rows:    # [m x n] * [n x p] = [m x p] i.e. [self.rows x other.cols] matrix
            other_cols = []
            for i in range(other.cols):  # extract columns from rows
                other_cols.append([row[i] if isinstance(other, Matrix) else row for row in other.comp])
            for row_me in self.comp:
                new_row = []
                for col_other in other_cols:
                    new_row.append(Vector(row_me) * Vector(col_other))   # Dot product of vectors
                new_matrix.append(new_row)
            return Vector([row[0] for row in new_matrix]) if other.cols == 1 else Matrix(new_matrix)
        else:
            raise ValueError("Size mismatch; [m x n] * [n x p] = [m x p] matrix")

    def __eq__(self, other):
        """
        If two matrices have the same components, then they are equal. If the
        lists are not the same length, will always be False with no error thrown.
        Have to compare each component due to necessity of using math.isclose()
        on floats in order to deal with floating point errors.

        :param other: other matrix being tested for equality
        :type other: Matrix
        :return: True or False based on equality
        :rtype: bool
        """
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for my_row, other_row in zip(self, other):
            for my_val, other_val in zip(my_row, other_row):
                if not isclose(my_val, other_val):
                    return False

        return self.comp == other.comp  # compares lists

    def __pow__(self, power, modulo=None):
        """
        Allows you to raise a matrix to a power, that is, each of the
        components of the current matrix is raised to a power. Can use
        power 0 to fill the current matrix with all 1s.

        :param power: value to raise each component to
        :param modulo: optional parameter that applies the modulus operator to each result
        :type power: int, float
        :type modulo: int, float
        :return: a matrix containing the appropriately scaled components
        :rtype: Matrix
        """
        new_comp = []
        for row in self.comp:
            new_row = []
            for elem in row:
                if modulo:
                    elem = elem % modulo
                new_row.append(pow(elem, power))
            new_comp.append(new_row)
        return Matrix(new_comp)

    def __str__(self):
        """
        String representation of matrix is each row separated by new line
        characters. This is done so that when printed it resembles a normal
        matrix as closely as possible.

        :return: string representation of current matrix
        :rtype: str
        """

        # joins each row of matrix with a new line character and a space,
        # floats are converted to visual fractions, need to get rid of quotes around them
        return "[" + '\n '\
            .join([str([str(Fraction(elem).limit_denominator()) if isinstance(elem, float) else elem for elem in row])
                  .replace('\'', '') for row in self.comp])\
            + "]"

    def __len__(self):
        """
        :return: returns tuple formatted as (row, col)
        :rtype: tuple
        """
        return self.rows, self.cols

    def __getitem__(self, index):
        """
        Allows user to access internal self.comp without doing
        my_matrix.comp[i][j] and instead doing my_matrix[i][j]

        Note: the first [] calls this function, which returns row,
                that row is a list, which supports [] in the same way
                that this function does.

        :param index: index of row
        :type index: int
        :return: list or value for row or row+col value
        :rtype: list, value
        """
        return self.comp[index]

    def __setitem__(self, key, value):
        """
        Allows the user to set a value using brackets.

        Note: behavior undefined if user attempts to set a row.

        :param key: index of row to be changed
        :param value: value to be set
        :type key: int
        :type value: int
        :return: no return
        """

        self.set(value, key)


if __name__ == "__main__":
    test()
