import requests
from zendesk.config import credentials, subdomain
from datetime import datetime

zendesk_api = 'zendesk.com/api/v2'


def create_welcome_message():
    payload = {
        'role': 'admin'
    }

    url = f'https://{subdomain}.{zendesk_api}/users.json'
    response = requests.get(url, params=payload, auth=credentials)
    user = response.json()['users'][0]['name']

    url = f'https://{subdomain}.{zendesk_api}/tickets/count.json'
    response = requests.get(url, auth=credentials)
    count = response.json()['count']['value']
    return user, count


def get_tickets():
    payload = {
        'query': 'type:ticket status:open',
        'sort_by': 'created_at',
        'sort_order': 'asc',
        'page[size]': '25'
    }

    url = f'https://{subdomain}.{zendesk_api}/tickets.json'
    response = requests.get(url, params=payload, auth=credentials)
    return response.json()['tickets']


def get_ticket(ticket_id):
    url = f'https://{subdomain}.{zendesk_api}/tickets/{ticket_id}'
    response = requests.get(url, auth=credentials)
    ticket = response.json()['ticket']
    print(ticket['subject'])
    return response.json()['ticket']


def parse_date(date):
    date = date[0:len(date) - 1]
    d = datetime.fromisoformat(date)
    return d.strftime("%A, %B %-d, %Y at %-I:%M %p")
