from __future__ import division
import numpy as np
from ..field import Field, CartesianGrid, UnstructuredCoords

def circular_aperture(diameter, center=None):
	'''Makes a Field generator for a circular aperture.

	Parameters
	----------
	diameter : scalar
		The diameter of the aperture.
	center : array_like
		The center of the aperture
	
	Returns
	-------
	Field generator
		This function can be evaluated on a grid to get a Field.
	'''
	if center is None:
		shift = np.zeros(2)
	else:
		shift = center * np.ones(2)

	def func(grid):
		if grid.is_('cartesian'):
			x, y = grid.coords
			f = ((x-shift[0])**2 + (y-shift[1])**2) <= (diameter / 2)**2
		else:
			f = grid.r <= (diameter / 2)
	
		return Field(f.astype('float'), grid)
	
	return func

def rectangular_aperture(size, center=None):
	'''Makes a Field generator for a rectangular aperture.

	Parameters
	----------
	size : scalar or array_like
		The length of the sides. If this is scalar, a square aperture is assumed.
	center : array_like
		The center of the aperture
	
	Returns
	-------
	Field generator
		This function can be evaluated on a grid to get a Field.
	'''
	dim = size * np.ones(2)
	
	if center is None:
		shift = np.zeros(2)
	else:
		shift = center * np.ones(2)

	def func(grid):
		x, y = grid.as_('cartesian').coords
		f = (np.abs(x-shift[0]) <= (dim[0]/2)) * (np.abs(y-shift[1]) <= (dim[1]/2))			
		return Field(f.astype('float'), grid)
	
	return func

def regular_polygon_aperture(num_sides, circum_diameter):
	'''Makes a Field generator for a regular-polygon-shaped aperture.

	Parameters
	----------
	num_sides : integer
		The number of sides for the polygon.
	circum_diameter : scalar
		The circumdiameter of the polygon.
	
	Returns
	-------
	Field generator
		This function can be evaluated on a grid to get a Field.
	'''
	if num_sides < 3:
		raise ValueError('The number of sides for a regular polygon has to greater or equal to 3.')
	
	apothem = np.cos(np.pi / num_sides) * circum_diameter / 2

	# Make use of symmetry
	if num_sides % 2 == 0:
		thetas = np.arange(int(num_sides / 2), dtype='float') * np.pi / int(num_sides / 2)
	else:
		thetas = np.arange(int(num_sides / 2) + 1) * (num_sides - 2) * np.pi / (num_sides / 2)

	mask = rectangular_aperture(circum_diameter*4)

	def func(grid):
		f = np.ones(grid.size, dtype='float')
		g = grid.as_('cartesian')
		m = mask(g) != 0

		x, y = g.coords
		x = x[m]
		y = y[m]

		f[~m] = 0

		# Make use of symmetry
		if num_sides % 2 == 0:
			for theta in thetas:
				f[m] *= (np.abs(np.cos(theta) * x + np.sin(theta) * y) < apothem)
		else:
			for theta in thetas:
				print(theta)
				f[m] *= ((np.abs(np.sin(theta) * x) + -np.cos(theta) * y) < apothem)
		
		return Field(f, grid)
	
	return func

# Convenience function
def hexagonal_aperture(circum_diameter):
	'''Makes a Field generator for a hexagon aperture.

	Parameters
	----------
	circum_diameter : scalar
		The circumdiameter of the polygon.
	
	Returns
	-------
	Field generator
		This function can be evaluated on a grid to get a Field.
	'''
	return regular_polygon_aperture(6, circum_diameter)

def segmented_aperture(subaperture_shape, subaperture_grid):
	'''Make a aperture with many similar subapertures.

	Parameters
	----------
	subaperture_shape : Field generator
		The shape of each subaperture.
	subaperture_grid : Grid
		The center of each of the subapertures.

	Returns
	-------
	Field generator
		The segmented aperture.
	'''
	def func(grid):
		ap = 0
		for p in subaperture_grid.points:
			ap += subaperture_shape(grid.shifted(-p))
		return Field(ap, grid)
	return func

def make_spider(p1, p2, spider_width):
	'''Make a rectangular obstruction from `p1` to `p2`.

	Parameters
	----------
	p1 : list or ndarray
		The starting coordinates of the spider.
	p2 : list or ndarray
		The end coordinates of the spider.
	spider_width : scalar
		The full width of the spider.
	
	Returns
	-------
	Field generator
		The spider obstruction.
	'''
	delta = np.array(p2) - np.array(p1)
	shift = delta / 2 + np.array(p1)

	spider_angle = np.arctan2(delta[1], delta[0])
	spider_length = np.linalg.norm(delta)

	spider = rectangular_aperture((spider_length, spider_width))

	def func(grid):
		x, y = grid.shifted(-shift).coords

		x_new = x * np.cos(spider_angle) + y * np.sin(spider_angle)
		y_new = y * np.cos(spider_angle) - x * np.sin(spider_angle)
		spider_grid = CartesianGrid(UnstructuredCoords([x_new, y_new]))

		return 1 - spider(spider_grid)
	return func

def make_spider_infinite(p, angle, spider_width):
	'''Make an infinite spider starting at `p` and extending at an angle `angle`.

	Parameters
	----------
	p : list or ndarray
		The starting coordinate of the spider.
	angle : scalar
		The angle to which the spider is pointing in degrees.
	spider_width : scalar
		The full width of the spider.

	Returns
	-------
	Field generator
		The spider obstruction.
	'''
	spider_angle = np.radians(angle)

	def func(grid):
		x,y = grid.shifted(p).coords

		x_new = x * np.cos(spider_angle) + y * np.sin(spider_angle)
		y_new = y * np.cos(spider_angle) - x * np.sin(spider_angle)
		infinite_spider = np.logical_or(np.abs(y_new) <= (spider_width / 2), x_new <= 0)

		return Field(1 - infinite_spider, grid)
	return func

def make_obstructed_circular_aperture(pupil_diameter, central_obscuration_ratio, num_spiders=0, spider_width=0.01):
	'''Make a simple circular aperture with central obscuration and support structure.

	Parameters
	----------
	pupil_diameter : scalar
		The diameter of the circular aperture.
	central_obscuration_ratio : scalar
		The ratio of the diameter of the central obscuration compared to the pupil diameter.
	num_spiders : int
		The number of spiders holding up the central obscuration.
	spider_width : scalar
		The full width of the spiders.
	
	Returns
	-------
	Field generator
		The circularly obstructed aperture.
	'''
	central_obscuration_diameter = pupil_diameter * central_obscuration_ratio

	def func(grid):	
		pupil_outer = circular_aperture(pupil_diameter)(grid)
		pupil_inner = circular_aperture(central_obscuration_diameter)(grid)
		spiders = 1

		spider_angles = np.linspace(0, 2*np.pi, num_spiders, endpoint=False)

		for angle in spider_angles:
			x = pupil_diameter * np.cos(angle)
			y = pupil_diameter * np.sin(angle)

			spiders *= make_spider((0, 0), (x, y), spider_width)(grid)
		
		return (pupil_outer - pupil_inner) * spiders
	return func
