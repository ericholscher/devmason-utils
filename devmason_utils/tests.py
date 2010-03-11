import pprint
import difflib
from django.test import TestCase, Client

from devmason_utils.utils import create_package, get_auth_string

class CreatePackageTests(TestCase):

    def test_create_package(self):
        auth = get_auth_string('test', 'test')
        resp = create_package('My Project', server='http://localhost:8000/devmason', auth=auth)
