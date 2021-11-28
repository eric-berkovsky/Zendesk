from django.shortcuts import render
from zendesk.functions import get_tickets, create_welcome_message


def index(request):
    tickets = get_tickets()
    user, total_ticket_count = create_welcome_message()
    prev_disabled = 'disabled' if 3 > 2 else False
    next_disabled = 'disabled' if 3 > 4 else False
    return render(request, 'index.html', {
        'user': user,
        'count': total_ticket_count,
        'tickets': tickets,
        'prev_disabled': prev_disabled,
        'next_disabled': next_disabled
    })


def ticket(request, ticket_id):
    return render(request, 'ticket.html', {
        'ticket_id': ticket_id
    })
