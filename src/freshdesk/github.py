'''
Github client
class GitUser(NamedTuple):
    login: str
    id: int
    node_id: str
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: str = "User"
    site_admin: Boolean = False
    name: str
    company: Optional[str]
    blog: Optional[str]
    location: Optional[str]
    email: str
    hireable: Optional[Boolean]
    bio: Optional[str]
    twitter_username: Optional[str]
    public_repos: Optional[int]
    public_gists: Optional[int]
    followers: Optional[int]
    following: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
'''
import logging
import os
from typing import Any, Dict

import requests

LOGGER = logging.getLogger(__name__)
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def get_user(username: str) -> Dict[str, Any]:
    '''
    :param username: github user name
    :return: user record
    '''
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise EnvironmentError("Missing env GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f'token {github_token}'
    }
    res = requests.get(f'https://api.github.com/users/{username}',
                        headers = headers)
    if res.status_code > 299:
        raise Exception(f"Unable to find user {username} in github.com")
    return res.json()
