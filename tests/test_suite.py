import unittest
from tests.test_actors import ActorsTestCase
from tests.test_movies import MoviesTestCase
from tests.test_permissions import TestPermissions

# Load test cases from separate test files
actors_tests = unittest.TestLoader().loadTestsFromTestCase(ActorsTestCase)
movies_tests = unittest.TestLoader().loadTestsFromTestCase(MoviesTestCase)
permission_tests = unittest.TestLoader().loadTestsFromTestCase(TestPermissions)

# Create test suite combining all test cases
all_tests = unittest.TestSuite([actors_tests, movies_tests, permission_tests])

# Run the test suite
if __name__ == '__main__':
    # Use TextTestRunner to run the tests with detailed verbosity
    unittest.TextTestRunner(verbosity=2).run(all_tests)
