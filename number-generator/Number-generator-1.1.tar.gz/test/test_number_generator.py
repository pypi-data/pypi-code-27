import unittest
from numbergenerator.number_generator import RandomGen


class TestNumberGenerator(unittest.TestCase):

    def test_size_invalid_input(self):

        # test invalid inputs are captured for variable size
        self.assertRaises(AssertionError, RandomGen, size='string_input')
        self.assertRaises(AssertionError, RandomGen, size=dict())
        self.assertRaises(AssertionError, RandomGen, size=[])
        self.assertRaises(AssertionError, RandomGen, size=1.3)
        self.assertRaises(AssertionError, RandomGen, size=-1)
        self.assertRaises(AssertionError, RandomGen, size=16)

    def test_random_numbers_invalid_input(self):

        # test invalid inputs are captured for variable random_numbers
        self.assertRaises(AssertionError, RandomGen, random_numbers='string_input')
        self.assertRaises(AssertionError, RandomGen, random_numbers=dict())
        self.assertRaises(AssertionError, RandomGen, random_numbers=1.3)
        self.assertRaises(AssertionError, RandomGen, random_numbers=[])
        self.assertRaises(AssertionError, RandomGen, random_numbers=[1, 2, 3])
        self.assertRaises(AssertionError, RandomGen, random_numbers=[0.1, 0.5, 3])
        self.assertRaises(AssertionError, RandomGen, random_numbers=[0.1, 0.5, 'string_input'])

    def test_probabilities_invalid_input(self):

        # test invalid inputs are captured for variable probabilities
        self.assertRaises(AssertionError, RandomGen, probabilities='string_input')
        self.assertRaises(AssertionError, RandomGen, probabilities=dict())
        self.assertRaises(AssertionError, RandomGen, probabilities=1.3)
        self.assertRaises(AssertionError, RandomGen, probabilities=[])
        self.assertRaises(AssertionError, RandomGen, probabilities=[1, 2, 3])
        self.assertRaises(AssertionError, RandomGen, probabilities=[0.1, 0.5, 3])
        self.assertRaises(AssertionError, RandomGen, probabilities=[0.1, 0.5, 'string_input'])

    def test_input_mismatch(self):

        # test error is correctly thrown when input size mismatch
        self.assertRaises(AssertionError, RandomGen, size=4, random_numbers=[0.2, 0.3, 0.5])
        self.assertRaises(AssertionError, RandomGen, size=4, probabilities=[0.2, 0.3, 0.5])
        self.assertRaises(AssertionError, RandomGen, random_numbers=[0.4, 0.2, 0.3, 0.5], probabilities=[0.2, 0.3, 0.5])

    def test_next_num_invalid_output(self):

        # test error is correctly thrown when input size mismatch
        rg = RandomGen()
        result = rg.next_num()
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 1)

    def test_run_multiple_invalid_input(self):

        # test error is correctly thrown when wrong input is specified
        rg = RandomGen()
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs='string_input')
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs=dict())
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs=1.3)
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs=[1, 2, 3])
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs=[])
        self.assertRaises(AssertionError, rg.run_multiple, number_of_runs=None)

if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestNumberGenerator)
    unittest.TextTestRunner(verbosity=1).run(suite)



