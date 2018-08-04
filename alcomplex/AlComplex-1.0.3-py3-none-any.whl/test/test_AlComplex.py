import unittest
from AlComplex import * 

a = AlComplex(0,1)
b = AlComplex(1,0)
c = AlComplex(1,1)
d = AlComplex(2,3)
e = AlComplex(1)

class TestComplexNumberOperations(unittest.TestCase):
	def test_initialization_and_equality(self):
		self.assertEqual(C(0,1), a)
		self.assertEqual(AlComplex(0,1), a)
	
	def test_AlComplex_addition(self):
		self.assertEqual(a+b, c)
		self.assertEqual(a-b, AlComplex(-1,1))

	def test_AlComplex_multiplication(self):
		self.assertEqual(d*d, AlComplex(-5,12))
		self.assertEqual(C(1,0)*C(0,1), C(0,1))

	def test_AlComplex_potentiation(self):
		self.assertEqual(i**2, -1)
		self.assertEqual((-1)**AlComplex(0,3), exp(-m.pi*3))
		self.assertEqual((-i)**i, exp(m.pi/2))

	def test_AlComplex_division(self):
		self.assertEqual(i/i, 1)
		self.assertEqual(AlComplex(1,0)/i, -i)

	def test_AlComplex_ops_plays_nicely_with_Python_native_types(self):
		self.assertEqual(3*C(9,8), C(27,24))
		
		self.assertEqual(j+4, C(4,1))
		self.assertEqual(j+4.123, C(4.123,1))
		self.assertEqual(j+m.sqrt(4.123), C(m.sqrt(4.123),1))
		self.assertEqual(3 + 1.j + a, C(3, 2))

		self.assertEqual(AlComplex(900)*4, AlComplex(3600))
		self.assertEqual((3-i)/(2+3*i)+(2-2*i)/(1-5*i), 9/13 - 7/13*i)
		
		self.assertEqual(C(4)**1/2, 2)
		
class TestLoneMethods(unittest.TestCase):
	def test_AlComplex_use_j(self):
		use_j()

		self.assertEqual(str(a), '0.0 + 1.0j')
		self.assertEqual(str(b), '1.0 + 0.0j')
		self.assertEqual(str(c), '1.0 + 1.0j')

		use_j(False)
		self.assertEqual(str(a), '0.0 + 1.0i')

	def test_real(self):
		self.assertEqual(real(a), 0)
		self.assertEqual(real(b), 1)
		self.assertEqual(real(c), 1)
		self.assertEqual(real(d), 2)
		self.assertEqual(real(e), 1)

	def test_real_on_python_types(self):
		self.assertEqual(real(1), 1)
		self.assertEqual(real(-1), -1)

		self.assertEqual(real(4.323), 4.323)
		self.assertEqual(real(m.pi), m.pi)

		self.assertEqual(real(1.j), 0)
		self.assertEqual(real(4 + 3.j), 4)

	def test_imag(self):
		self.assertEqual(imaginary(a), 1)
		self.assertEqual(imaginary(b), 0)
		self.assertEqual(imaginary(c), 1)
		self.assertEqual(imaginary(d), 3)
		self.assertEqual(imaginary(e), 0)

	def test_imag_on_python_types(self):
		self.assertEqual(imaginary(1), 0)

		self.assertEqual(imaginary(1.j), 1)
		self.assertEqual(imaginary(4 + 3.j), 3)

	def test_sqrt(self):
		self.assertEqual(sqrt(a), a**.5)
		self.assertEqual(sqrt(C(-1)), i)
		self.assertEqual(sqrt(C(4)), 2)

		self.assertEqual(sqrt(4), 2)
		self.assertEqual(sqrt(-1), 1.j)

	def test_inverse(self):
		self.assertEqual(inverse(a), 1/a)
		self.assertEqual(inverse(a), a**-1)

		self.assertEqual(inverse(C(2)), .5)
		self.assertEqual(inverse(c), .5 - .5*i)

		self.assertEqual(inverse(2), .5)
		self.assertEqual(inverse(4.j), -0.25*1.j)

	def test_exp(self):
		self.assertEqual(exp(1), m.exp(1))
		self.assertEqual(exp(0), 1)
		self.assertEqual(exp(0+m.pi*i), -1)
		self.assertEqual(exp(m.log(3) - m.pi/2*i), C(0,-3))
		self.assertEqual(4*exp(m.pi/4*i), AlComplex.polar(4, m.pi/4))
		self.assertEqual(exp(m.pi*1.j), -1)

	def test_Ln(self):
		self.assertEqual(Ln(1), 0)
		self.assertEqual(Ln(exp(4+i)), 4+i)
		self.assertEqual(Ln(-1), m.pi*i)
		self.assertEqual(Ln(-i), -m.pi/2*i)

	def test_exponential(self):
		self.assertEqual(i**-1, -i)
		self.assertEqual(C(4)**-1, 1/4)
		self.assertEqual(1.j**-1, -i)

	def test_trigonometric_sin_cos_tan(self):
		self.assertEqual(sin(0), 0)
		self.assertEqual(sin(m.pi/2), 1)
		self.assertEqual(sin(4*i), 1/2*(m.exp(4)-m.exp(-4))*i)
		
		self.assertEqual(cos(0), 1)
		self.assertEqual(cos(m.pi), -1)
		
		self.assertEqual(tan(0), 0)
		self.assertEqual(tan(1+i), sin(1+i)/cos(1+i))
		self.assertEqual(tan(m.pi/4), 1)
		self.assertEqual(tan(1+1.j), sin(1+1.j)/cos(1+1.j))

	def test_trigonometric_sec_csc_cot(self):
		self.assertEqual(sec(0), 1)
		self.assertEqual(sec(m.pi), -1)
		self.assertEqual(sec(4*i), 1/cos(4*i))
		
		self.assertEqual(csc(1.5*m.pi), -1)
		self.assertEqual(csc(m.pi/2), 1)
		self.assertEqual(csc(7+2*i), 1/sin(C(7,2)))
		
		self.assertEqual(cot(m.pi/4), 1)
		self.assertEqual(cot(1+i), cos(1+i)/sin(1+i))
		self.assertEqual(cot(1+i), csc(1+i)/sec(1+i))

	def test_hyperbolic_trigonometric_sinh_cosh_tanh(self):
		self.assertEqual(-i*sinh(i*a), sin(a))
		self.assertEqual(sinh(c), -i*sin(i*c))

		self.assertEqual(cos(b), cosh(i*b))
		self.assertEqual(cosh(d), cos(d*i))

		self.assertEqual(tanh(0), 0)
		self.assertEqual(tanh(4*i), sinh(4*i)/cosh(4*i))

	def test_hyperbolic_trigonometric_sech_csch_coth(self):
		self.assertEqual(sech(i*a), sec(a))
		self.assertEqual(sech(c+d), 1/cosh(c+d))

		self.assertEqual(csch(b), i*csc(i*b))
		self.assertEqual(csch(d), 1/sinh(d))

		self.assertEqual(coth(a+b), 1/tanh(a+b))
		self.assertEqual(coth(4*i), csch(4*i)/sech(4*i))

	def test_inverse_trig_asin_acos_atan(self):
		self.assertEqual(asin(0), 0)
		self.assertEqual(asin(1), m.pi/2)
		self.assertEqual(asin(C(2,3)), cm.asin(2+3.j))

		self.assertEqual(acos(0), m.pi/2)
		self.assertEqual(acos(1), 0)
		self.assertEqual(acos(C(2,3)), cm.acos(2+3.j))

		self.assertEqual(atan(1), m.pi/4)
		self.assertEqual(atan(0), 0)
		self.assertEqual(atan(C(2,3)), cm.atan(2+3.j))

	def test_inverse_hyper_trig_asinh_acosh_atanh(self):
		self.assertEqual(acosh(2+3.j), cm.acosh(2+3.j))
		self.assertEqual(asinh(2+3.j), cm.asinh(2+3.j))
		self.assertEqual(atanh(2+3.j), cm.atanh(2+3.j))

	def test_int_roots(self):
		l1 = list(int_roots(1, 3))
		l2 = list(int_roots(1.j, 2))
		l5 = list(int_roots(i+2, 10))

		self.assertEqual(len(l1), 3)
		self.assertEqual(len(l5), 10)
		self.assertEqual(l1[0]**3, 1)
		self.assertEqual(l2[1]**2, i)
		self.assertEqual(l5[3]**10,i+2)

	def test_int_roots_raises_ValueError(self):
		with self.assertRaises(ValueError):
			int_roots(i, 0)

	def test_ln_n_branch(self):
		self.assertEqual(ln_n_branch(1,0), 0)
		self.assertEqual(ln_n_branch(exp(4+i), 0), 4+i)
		self.assertEqual(ln_n_branch(exp(4+i), 1), 4+i+2*m.pi*i)

	def test_ln_n_branch_raises_ValueError(self):
		with self.assertRaises(ValueError):
			ln_n_branch(i, 4.3)

	def test_ln_values(self):
		l1 = list(ln_values(i+12, 3, 7))
		l2 = list(ln_values(i, 6, 2))
		l3 = list(ln_values(i, -2, 3))

		self.assertEqual(len(l1), len(l2))
		for k in l1:
			self.assertEqual(exp(k), i+12)

		self.assertIn(-7*m.pi/2*i, l3)
		self.assertIn(-3*m.pi/2*i, l3)
		self.assertIn(m.pi/2*i, l3)
		self.assertIn(5*m.pi/2*i, l3)

	def test_ln_values_raises_ValueErrors(self):
		with self.assertRaises(ValueError):
			ln_values(i, "ay")
		with self.assertRaises(ValueError):
			ln_values(i, 2, 2.4)
		with self.assertRaises(ValueError):
			ln_values(i, m, 4)

	def test_lone_methods_with_Python_number_types(self):
		# Conjugate
		self.assertEqual(conjugate(1), 1)
		self.assertEqual(conjugate(3.j), -3.j)

		# Modulus
		self.assertEqual(modulus(2), 2)
		self.assertEqual(modulus(2.34), 2.34)
		self.assertEqual(modulus(3 + 4.j), 5)

		# Phase
		self.assertEqual(phase(3), 0)
		self.assertEqual(phase(1.j), m.pi/2)

class TestAlComplexClassMethods(unittest.TestCase):
	def test_modulus_abs_magnitude(self):
		self.assertEqual(a.modulus(), 1.0)
		self.assertEqual(b.abs(), 1.0)
		self.assertEqual(c.magnitude(), sqrt(2))
		self.assertEqual(abs(e), 1.0)

	def test_to_rect_coord(self):
		self.assertEqual(a.to_rect_coord(), (0, 1))
		self.assertEqual(b.to_rect_coord(), (1, 0))
		self.assertEqual(c.to_rect_coord(), (1, 1))
		self.assertEqual(d.to_rect_coord(), (2, 3))
		self.assertEqual(e.to_rect_coord(), (1, 0))

	def test_to_float_raises_TypeError_if_imaginary_part_not_zero(self):
		with self.assertRaises(TypeError):
			d.to_float()	

	def test_to_int_raises_TypeError_if_imaginary_part_not_zero(self):
		with self.assertRaises(TypeError):
			d.to_int()