import random
import numpy as np


class RandomGen:

    @property
    def size(self):
        # get value
        return self._size

    @property
    def random_numbers(self):
        # get value
        return self._random_numbers

    @property
    def probabilities(self):
        # get value
        return self._probabilities

    @size.setter
    def size(self, value):

        # assert input value is valid
        assert isinstance(value, int), 'Input must be a scalar value'
        assert 0 < value < 15, 'Input value must be between 0 and 15'

        # set value
        self._size = value

    @random_numbers.setter
    def random_numbers(self, value):

        # assert input value is valid
        assert isinstance(value, list), TypeError('random_numbers must be a list')
        assert all([isinstance(x, float) for x in value]), 'Every list component must be a float'
        assert all([0 <= x <= 1 for x in value]), 'Every list component must be a float between 0 and 1'
        assert len(value) == self.size, 'random_numbers size must match size value'
        assert len(value) == self.size, 'Input size must match "size" parameter value'

        # set value
        self._random_numbers = value

    @probabilities.setter
    def probabilities(self, value):

        # assert input value is valid
        assert isinstance(value, list), 'Input must be a list'
        assert all([isinstance(x, float) for x in value]), 'Every list component must be a float'
        assert all([0 <= x <= 1 for x in value]), 'Every list component must be a float between 0 and 1'
        assert len(value) == self.size, 'Input size must match "size" parameter value'

        # set value
        self._probabilities = value

    def __init__(self, **kwargs):

        """RandomGen constructor allows user to specify the values to be outputted
         as well as their associated probabilities. If no input is provided values
         and probabilities will automatically be generated.

        Inputs:
            size: integer between o and 15
            random_numbers = list of float values between 0 and 1. List length must match the size value
            probabilities = list of float values between 0 and 1. List length must match the size value"""

        # initialise properties
        self._size = None
        self._random_numbers = None
        self._probabilities = None

        # Get properties
        size = kwargs.get('size', None)
        random_numbers = kwargs.get('random_numbers', None)
        probabilities = kwargs.get('probabilities', None)
        self.results = []

        # check if attributes have been inputted, otherwise create attribute values
        if size is None:

            if random_numbers is not None and isinstance(random_numbers, list):
                self.size = len(random_numbers)
            elif probabilities is not None and isinstance(probabilities, list):
                self.size = len(probabilities)
            else:
                self.size = 4
        else:
            self.size = size

        if random_numbers is None:
            self.random_numbers = [round(random.random(), 2) for _ in range(0, self.size)]
        else:
            self.random_numbers = random_numbers

        if probabilities is None:

            probabilities = [None] * self.size

            # Probability of the occurrence of random_nums
            remaining_probability = 100
            indexes = range(self.size)
            random_index = random.sample(indexes, len(indexes))
            for ii in range(self.size):

                if not ii == len(self.random_numbers) - 1:
                    new_probability = random.randrange(0, remaining_probability, 1)
                    remaining_probability = remaining_probability - new_probability
                    probabilities[random_index[ii]] = new_probability / 100
                else:
                    probabilities[random_index[ii]] = remaining_probability / 100

            self.probabilities = probabilities

        else:
            self.probabilities = probabilities

    def next_num(self):

        """
        next_num method retrieves a value within the random_numbers list based
        on the probabilities associated to each number.

        Output is always a number existing within the random_number list.
        """
        return np.random.choice(self.random_numbers, p=self.probabilities)

    def run_multiple(self, number_of_runs):

        """
        run_multiple method runs next_num method multiple times and
        print the number of occurrences of a particular number vs their probability

        Inputs:
            number_of_runs: must be an integer that specifies the number of times
            next_num is executed
        """

        # assert input is provided in the right format
        assert isinstance(number_of_runs, int), ' Input must be an integer greater than 0'
        assert number_of_runs > 0, ' Input must be an integer greater than 0'

        for i in range(number_of_runs):
            self.results.append(self.next_num())

        # create output display
        for ii, this_value in enumerate(self.random_numbers):
            times_in_list = self.results.count(this_value)
            print('Value ' + str(this_value) + ': ' + str(times_in_list) + ' times' +
                  ' (Probability: ' + str(self.probabilities[ii]) + ')')

if __name__ == "__main__":
    rg = RandomGen(size=5)
    rg.run_multiple(1000)
