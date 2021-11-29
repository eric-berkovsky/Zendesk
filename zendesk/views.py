from django.shortcuts import render, redirect
from zendesk.functions import *


def index(request):
    try:
        prev_page, next_page = False, False
        if request.method == 'POST':
            if 'previous' in request.POST:
                prev_page = True
            elif 'next' in request.POST:
                next_page = True

        tickets_json = get_tickets(prev_page, next_page)
        tickets = tickets_json['tickets']
        on_page_count = len(tickets)

        user, total_ticket_count = create_welcome_message()
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
        return render(request, 'error.html', {'error_message': 'The API seems to be down. Please try again later.'})
    except PermissionError:
        return render(request, 'error.html', {'error_message': 'There was an issue with your request. Please confirm '
                                                               'your credentials and that you have permission to view'
                                                               ' this resource.'})


def ticket(request, ticket_id):
    try:
        zendesk_ticket = get_ticket(ticket_id)
        return render(request, 'ticket.html', {
            'ticket_id': zendesk_ticket['id'],
            'requester': get_user_name(zendesk_ticket['requester_id']),
            'status': zendesk_ticket['status'],
            'date': parse_date(zendesk_ticket['created_at']),
            'subject': zendesk_ticket['subject'],
            'description': zendesk_ticket['description'],
        })
    except RuntimeError:
        return render(request, 'error.html', {'error_message': 'The API seems to be down. Please try again later.'})
    except PermissionError:
        return render(request, 'error.html', {'error_message': 'There was an issue with your request. Please confirm '
                                                               'your credentials and that you have permission to view'
                                                               ' this resource.'})


def error(request, error_message):
    return render(request, 'error.html', {'error': error_message})
