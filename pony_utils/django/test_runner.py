from django.test.simple import DjangoTestSuiteRunner
from pony_utils.django.utils import report_results_for_suite

class PonyReportRunner(DjangoTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None):
        """
        Run the Django test suite and report results to pony_server.
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        old_config = self.setup_databases()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        #This is the only line changed.
        report_results_for_suite(suite, result)
        return self.suite_result(result)
