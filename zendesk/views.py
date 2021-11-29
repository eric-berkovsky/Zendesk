from django.shortcuts import render
from zendesk.functions import *

api_error_message = 'The Zendesk API seems to be down. Please try again later.'
user_error_message = 'There was an issue with your request. Please confirm your credentials were entered correctly ' \
                     'and that you have permission to view this resource.'


def index(request):
    """
    Loads the home page which displays up to 25 tickets at a time and allows the user to requests to see previous and
    next tickets through buttons
    @param request: The HTTP request
    @return: The home page with up to 25 tickets
    """
    try:
        # Record if the user asked for the previous or next page
        user_wants_prev_page, user_wants_next_page = False, False
        if request.method == 'POST':
            if 'previous' in request.POST:
                user_wants_prev_page = True
            elif 'next' in request.POST:
                user_wants_next_page = True

        # Get the tickets to display - from the previous or next page if requested
        tickets_json = get_tickets(user_wants_prev_page, user_wants_next_page)
        tickets = tickets_json['tickets']

        # Get user's name, total ticket count, and number of tickets currently displayed (up to 25)
        user = get_admin_name()
        total_ticket_count = get_total_ticket_count()
        on_page_count = len(tickets)

        # Set variables which will disable the previous or next button if needed
        prev_disabled = 'disabled' if not has_prev_tickets(tickets_json['links']['prev']) else ''
        next_disabled = 'disabled' if not tickets_json['meta']['has_more'] else ''

        return render(request, 'index.html', {
            'user': user,
            'count': total_ticket_count,
            'tickets': tickets,
            'on_page': on_page_count,
            'prev_disabled': prev_disabled,
            'next_disabled': next_disabled
        })
    except RuntimeError:
        return render(request, 'error.html', {'error_message': api_error_message})
    except PermissionError:
        return render(request, 'error.html', {'error_message': user_error_message})


def ticket(request, ticket_id):
    """
    Loads a web page showing information for a specific ticket
    @param request: The HTTP request
    @param ticket_id: The ID of the ticket to be displayed on this page
    @return: A webpage with information for the ticket with the given ID
    """
    try:
        zendesk_ticket = get_ticket(ticket_id)
        print(type(zendesk_ticket))
        return render(request, 'ticket.html', {
            'ticket_id': zendesk_ticket['id'],
            'requester': get_user_name(zendesk_ticket['requester_id']),
            'status': zendesk_ticket['status'],
            'date': parse_date(zendesk_ticket['created_at']),
            'subject': zendesk_ticket['subject'],
            'description': zendesk_ticket['description'],
        })
    except RuntimeError:
        return render(request, 'error.html', {'error_message': api_error_message})
    except PermissionError:
        return render(request, 'error.html', {'error_message': user_error_message})


def error(request, error_message):
    """
    Loads an error page if an HTTP request was unsuccessful
    @param request: The HTTP request
    @param error_message: A message describing what went wrong (such as API down or user error)
    @return: A webpage with the error message
    """
    return render(request, 'error.html', {'error': error_message})
