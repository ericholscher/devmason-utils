import unittest
from django.conf import settings
from django.db.models import get_app, get_apps
from django.test import _doctest as doctest
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.testcases import OutputChecker, DocTestRunner, TestCase
from django.test.simple import *

from devmason_utils.django_utils import report_results_for_suite

def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    """
    Run the unit tests for all the test labels in the provided list.
    Labels must be of the form:
     - app.TestClass.test_method
        Run a single specific test method
     - app.TestClass
        Run all the test methods in a given class
     - app
        Search for doctests and unittests in the named application.

    When looking for tests, the test runner will look in the models and
    tests modules for the application.

    A list of 'extra' tests may also be provided; these tests
    will be added to the test suite.

    Returns the number of tests that failed.
    """
    setup_test_environment()

    settings.DEBUG = False
    suite = unittest.TestSuite()

    if test_labels:
        for label in test_labels:
            if '.' in label:
                suite.addTest(build_test(label))
            else:
                app = get_app(label)
                suite.addTest(build_suite(app))
    else:
        for app in get_apps():
            #run_tests(build_suite(app))
            suite.addTest(build_suite(app))

    for test in extra_tests:
        suite.addTest(test)

    suite = reorder_suite(suite, (TestCase,))

    old_name = settings.DATABASE_NAME
    from django.db import connection
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    connection.creation.destroy_test_db(old_name, verbosity)

    teardown_test_environment()

    report_results_for_suite(suite, result)

    return len(result.failures) + len(result.errors)
