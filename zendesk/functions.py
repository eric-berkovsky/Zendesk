import requests
from zendesk.config import credentials, subdomain
from datetime import datetime

zendesk_api = 'zendesk.com/api/v2'
url_cursor = f'https://{subdomain}.{zendesk_api}/tickets.json'


def get_api_response(url, payload=None):
    """
    Helper method which calls the Zendesk API given the url and optional parameters
    Throws exceptions if there was an issue with the response which are caught in views.py
    Provides a way to funnel all errors through one method
    @param url: URL in Zendesk API to query
    @param payload: Optional parameters for the HTTP request
    @return: The HTTP response
    """
    response = requests.get(url, params=payload, auth=credentials)
    if response.status_code >= 500:
        # If the status code is in the 500s this means Zendesk's API is probably unavailable
        raise RuntimeError
    elif response.status_code >= 400:
        # If the status code is in the 400s this is likely a user error or insufficient permissions
        raise PermissionError
    else:
        return response


def get_admin_name():
    """
    Gets the name of the person using this application
    Used to display a welcome message in the web app's home page
    @return: User's name
    """
    payload = {
        'role': 'admin'
    }

    url = f'https://{subdomain}.{zendesk_api}/users.json'
    response = get_api_response(url, payload)
    return response.json()['users'][0]['name']


def get_total_ticket_count():
    """
    Gets the total number of tickets the user of this web app has
    Used to display a welcome message in the web app's home page
    @return: User's total ticket count
    """
    url = f'https://{subdomain}.{zendesk_api}/tickets/count.json'
    response = get_api_response(url)
    return response.json()['count']['value']


def get_tickets(user_wants_prev_page, user_wants_next_page):
    """
    Returns up to 25 tickets for display on the home page. Uses Zendesk's cursor-based pagination method.
    If needed, updates the global url_cursor variable which holds the current cursor in the list of all tickets
    @param user_wants_prev_page: Goes to the previous page if the user clicked the Previous button
    @param user_wants_next_page: Goes to the next page if the user clicked the Next button
    @return: The requested tickets in JSON format
    """
    payload = {
        'page[size]': '25'
    }

    global url_cursor
    response = get_api_response(url_cursor, payload)
    data = response.json()
    if user_wants_prev_page:
        url_cursor = data['links']['prev']
    elif user_wants_next_page:
        url_cursor = data['links']['next']

    response = get_api_response(url_cursor, payload)
    return response.json()


def has_prev_tickets(prev_link):
    """
    Checks if there are previous tickets in the list according to current cursor location
    Used to determine whether the Previous button is enabled for the user
    @param prev_link: URL to previous 25 tickets
    @return: Boolean value representing whether the user can view previous tickets
    """
    response = requests.get(prev_link, auth=credentials)
    return len(response.json()['tickets']) > 0


def get_ticket(ticket_id):
    """
    Retrieves information about a specific ticket. Called when the user clicks the "View Ticket" link.
    @param ticket_id: The ID of the ticket the user is requesting
    @return: Information about the requested ticket as a Python dictionary
    """
    url = f'https://{subdomain}.{zendesk_api}/tickets/{ticket_id}'
    response = get_api_response(url)
    return response.json()['ticket']


def parse_date(date):
    """
    Converts the date provided by the Zendesk API into a human readable string for display on the site
    @param date: Date provided by Zendesk API (ticket's created_at field)
    @return: Human readable version of the date
    """
    d = datetime.fromisoformat(date[0:len(date) - 1])
    return d.strftime("%A, %B %-d, %Y at %-I:%M %p")


def get_user_name(user_id):
    """
    Get the user's name based on their ID. Used to see who the requester is for tickets.
    @param user_id: User's ID on zendesk
    @return: The full name of the user associated with this ID
    """
    url = f'https://{subdomain}.{zendesk_api}/users/{user_id}.json'
    response = get_api_response(url)
    return response.json()['user']['name']
