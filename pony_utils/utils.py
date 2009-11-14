try:
    import json
except:
    import simplejson
import httplib2
import distutils.util
import unicodedata
import re

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '_', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

def get_app_name_from_test(test):
    try:
        #doctest
        app = test._dt_test.name.split('.tests.')[0]
    except AttributeError:
        #unit test in tests
        app = test.__module__.split('.tests.')[0]
        if not app:
            #Unit test in models.
            app = test.__module__.split('.models.')[0]
        if not app:
            app = test.__module__.split('.')[0]
    return app


def get_arch():
    return distutils.util.get_platform()

def create_package(server, project, name=None, auth=None):
    if not name:
        name = project
    print "Sending info for %s" % name
    create_url = "%s/%s" % (server, slugify(unicode(project)))
    json_payload = '{"name": "%s"}' % name
    h = httplib2.Http()
    resp, content = h.request(create_url, "PUT", body=json_payload,
        headers={'content-type':'application/json',
                 'AUTHORIZATION': auth}
            )

def send_results(server, project, result_dict, auth=None):
    post_url = "%s/%s/builds" % (server, slugify(unicode(project)))
    json_payload = json.dumps(result_dict)
    h = httplib2.Http()
    resp, content = h.request(post_url, "POST", body=json_payload,
        headers={'content-type':'application/json',
                 'AUTHORIZATION': auth}
            )

def send_build_request(server, project, identifier):
    post_url = "%s/builds/request" % server
    post_data = json.dumps({
            'project': project,
            'identifier': identifier,
        })
    h = httplib2.Http()
    resp, content = h.request(post_url, "POST", body=post_data,
        headers={'content-type':'application/json'}
            )
