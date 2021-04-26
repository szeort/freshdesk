"""
That module is a freshdesk API client
"""
import json
import os
from typing import Any, Dict, List, NamedTuple, Optional

import requests

HEADERS = {"Content-Type" : "application/json"}


class Contact(NamedTuple):
    '''
    Freshdesk contact named tuple
    '''
    name: str
    email: str
    company_id: Optional[int]
    view_all_tickets: bool
    id: Optional[int] = None
    custom_fields: Optional[Dict[str, Any]] = None
    active: bool = False
    address: Optional[str] = None
    avatar: Optional[Dict[str, Any]] = None
    deleted: bool = False
    description: Optional[str] = None
    job_title: Optional[str] = None
    language: Optional[str] = None
    mobile: Optional[str] = None
    other_emails: Optional[List[str]] = None
    phone: Optional[str] = None
    tags: Optional[List[str]] = None
    time_zone: Optional[str] = None
    twitter_id: Optional[str] = None
    unique_external_id: Optional[str] = None
    other_companies: Optional[List[Dict]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


def _apikey() -> str:
    '''
    Internal helper function to retreive token
    :return: freshdesk token
    '''
    freshdesk_token = os.environ.get('FRESHDESK_TOKEN')
    if not freshdesk_token:
        raise EnvironmentError('No freshdesk token in env')
    return freshdesk_token

def find_contact_by_email(domain: str, email: str) -> Optional[Contact]:
    '''
    :param domain: freshdesk domain
    :param email: user email
    :return: Contact or None
    '''
    #pylint: disable=line-too-long
    res = requests.get(f'https://{domain}.freshdesk.com/api/v2/search/contacts?query="email:{email}"',
                       auth = (_apikey(), 'x'),
                       headers = HEADERS)
    if res.status_code > 299:
        raise Exception('+'.join(res.json().get("errors")))
    if res.json().get('total') > 0:
        return Contact(**res.json()['results'][0])
    return None


def create_contact(domain: str, contact: Contact) -> Contact:
    '''
    :param domain: freshdesk domain
    :param contact:Contact object to be created via API
    :return: Contact
    '''
    res = requests.post(f'https://{domain}.freshdesk.com/api/v2/contacts',
                        auth = (_apikey(), 'x'),
                        data = json.dumps(contact._asdict()),
                        headers = HEADERS)
    if res.status_code > 299:
        raise Exception('+'.join(res.json().get("errors")))
    return Contact(**res.json())


def update_contact(domain: str, contact: Contact) -> Contact:
    '''
    :param domain: freshdesk domains
    :param contact:Contact object to be updated via API
    :return: Contact
    '''
    data = contact._asdict()
    del data['id']
    res = requests.put(f'https://{domain}.freshdesk.com/api/v2/contacts',
                        auth = (_apikey(), 'x'),
                        data = json.dumps(data),
                        headers = HEADERS)
    if res.status_code > 299:
        raise Exception('+'.join(res.json().get("errors")))
    return Contact(**res.json())


def find_company_id_by_name(domain: str, name: Optional[str]) -> Optional[int]:
    '''
    :param name: company name
    :return: company ID or None
    '''
    company_id: Optional[int] = None
    if not name:
        return company_id
    res = requests.get(f'https://{domain}.freshdesk.com//api/v2/companies/autocomplete?name={name}',
                        auth = (_apikey(), 'x'),
                        headers = HEADERS)
    if res.status_code > 299:
        raise Exception('+'.join(res.json().get("errors")))
    companies = res.json().get('companies')
    if companies:
        company_id = companies[0]['id']
    return company_id
