import unittest

if __name__ == "__main__":
    # Lauch all the unitary tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')

    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)