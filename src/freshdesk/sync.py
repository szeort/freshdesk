'''
Orchestration logic, cmd entry function main()
'''
import argparse
import logging
import sys
from typing import Any, Dict, Optional, cast

import freshdesk.api as api
import freshdesk.github as github

LOGGER = logging.getLogger(__name__)


def sync(username: str, domain: str):
    '''
    :param username: github username as string
    :param domain: freshdesk domain as string
    :return: None
    '''
    contact: Optional[api.Contact] = None
    company_id: Optional[int] = None
    gituser: Dict[str, Any] = github.get_user(username)
    email = gituser.get('email')
    if email is None:
        raise Exception("Email of the github user not visible")
    company_name: Optional[str] = cast(Optional[str], gituser.get('company'))
    try:
        company_id = api.find_company_id_by_name(domain, company_name)
    except Exception: # pylint: disable=broad-except
        LOGGER.exception("Error retreiving company %s", gituser.get('company'))
    contact = api.find_contact_by_email(domain, email)
    if contact is None:
        contact_data = {
            'active': True,
            'avatar': {
                'avatar_url': gituser.get('avatar_url')
            },
            'company_id': company_id,
            'view_all_tickets': True,
            'description': "copied from github.com",
            'email': email,
            'name': gituser.get('name')
        }
        contact = api.Contact(**contact_data)
        api.create_contact(domain, contact)
    else:
        #pylint: disable=line-too-long
        updated = contact._replace(avatar={'avatar_url': gituser.get('avatar_url')}, company_id=company_id)
        api.update_contact(domain, updated)

def main():
    '''
    Main entry for the cmd script
    '''
    parser = argparse.ArgumentParser(description='Git to Freshdesk synchronizer')
    parser.add_argument('user', type=str, help='git username')
    parser.add_argument('domain', type=str, help='target freshdesk domain')
    args = parser.parse_args()

    try:
        sync(args.user, args.domain)
    except Exception as err: #pylint: disable=broad-except
        print(err)
        sys.exit(2)
