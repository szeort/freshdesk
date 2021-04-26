import json
import pkg_resources


DISPATCHER = {
    'GET': {
        'https://api.github.com/users/octocat': 'github_user.json',
        'https://mockdomain.freshdesk.com/api/v2/search/contacts?query="email:octocat@github.com"': 'contact_list_empty.json'
    },
    'POST': {
        'https://mockdomain.freshdesk.com/api/v2/contacts': 'created_contact.json'
    },
    'PUT':{
    }
}

class MockResponse:
    def __init__(self, code, content):
        self.code = code
        self.content = content

    def json(self):
        return json.loads(self.content)

    @property
    def status_code(self):
        return self.code


def _serve(method, url):
    res_name = DISPATCHER[method].get(url)
    if res_name is None:
        return MockResponse(404, '{"errors": ["Not found"]}')
    return MockResponse(200, pkg_resources.resource_string(__name__, res_name))


def get(url, headers=None, auth=None):
    return _serve('GET', url)


def post(url, headers=None, auth=None, data=None):
    return _serve('POST', url)


def put(url, headers=None, auth=None):
    return _serve('PUT', url)
