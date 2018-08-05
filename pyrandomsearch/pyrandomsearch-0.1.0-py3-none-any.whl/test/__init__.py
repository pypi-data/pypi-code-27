import unittest

def get_test_suite():
    '''
    This is adapted from https://stackoverflow.com/a/37033551. The
    documentation for setup.py's test_suite is lacking.
    '''
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.', pattern='test_*.py')
    return test_suite
