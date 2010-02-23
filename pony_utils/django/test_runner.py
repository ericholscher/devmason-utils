from django.test.simple import DjangoTestSuiteRunner
from pony_utils.django.utils import report_results_for_suite

class PonyReportRunner(DjangoTestSuiteRunner):
    def suite_result(self, suite, result, **kwargs): 
        report_results_for_suite(suite, result)
        return self.suite_result(result)
