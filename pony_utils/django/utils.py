from django.conf import settings
import datetime
import socket
import unittest

from pony_utils.utils import create_package, send_results, get_arch, get_app_name_from_test

PB_SERVER = getattr(settings, 'PB_SERVER', 'http://devmason.com/pony_server')
PB_USER = getattr(settings, 'PB_USER', '')
PB_PASS = getattr(settings, 'PB_PASS', '')
if PB_USER and PB_PASS:
    PB_AUTH = "Basic %s" % ("%s:%s" % (PB_USER, PB_PASS)).encode("base64").strip()
else:
    print "No auth provided."
    PB_AUTH = None

STARTED = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

def _insert_failure(failed_apps, app, failure):
    if failed_apps.has_key(app):
        failed_apps[app].append(failure)
    else:
        failed_apps[app] = [failure]

def _increment_app(all_apps, app):
    if all_apps.has_key(app):
        all_apps[app] += 1
    else:
        all_apps[app] = 1

def get_test_cases(suite):
    test_cases = []
    if isinstance(suite, unittest.TestSuite):
        for test_case_or_suite in suite._tests:
            if isinstance(test_case_or_suite, unittest.TestSuite):
                test_cases.extend(get_test_cases(test_case_or_suite))
            else:
                test_cases.append(test_case_or_suite)
    return test_cases

def report_results_for_suite(suite, result):
    failed_apps = {}
    all_apps = {}
    for test in get_test_cases(suite):
        test_app = get_app_name_from_test(test)
        _increment_app(all_apps, test_app)
    for failure in result.failures + result.errors:
        test = failure[0]
        output = failure[1]
        app = get_app_name_from_test(test)
        _insert_failure(failed_apps, app, failure)

    arch = get_arch()
    hostname = socket.gethostname()

    for app in all_apps:
        success = app not in failed_apps.keys()
        if app in failed_apps:
            errout = '\n'.join([failure[1] for failure in failed_apps[app]])
        else:
            errout = "%s Passed" % all_apps[app]
        build_dict = {'success': success,
                        'started': STARTED,
                        'finished': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
                        'tags': ['django_test_runner'],
                        'client': {
                            'arch': arch,
                            'host': hostname,
                            'user': PB_USER,
                                },
                        'results': [
                           {'success': success,
                            'name': 'Test Application',
                            'errout': errout,
                            'started': STARTED,
                            'finished': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
                           }
                        ]
                    }

        create_package(app, server=PB_SERVER, auth=PB_AUTH)
        send_results(app, build_dict, server=PB_SERVER, auth=PB_AUTH)
