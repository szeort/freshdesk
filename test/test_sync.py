import os
import unittest
import unittest.mock
import mock_request
from freshdesk.sync import sync


class TestSync(unittest.TestCase):

    @unittest.mock.patch.dict(os.environ, {
        'GITHUB_TOKEN': 'mock_github_token',
        'FRESHDESK_TOKEN': 'mock_freshdesk_token'
    })
    @unittest.mock.patch("requests.get", new=mock_request.get)
    @unittest.mock.patch("requests.post", new=mock_request.post)
    def test_sync(self):
        #mock_get.side_effect = mock_request.get
        sync('octocat', 'mockdomain')
