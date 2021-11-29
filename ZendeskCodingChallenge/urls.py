"""ZendeskCodingChallenge URL Configuration
"""
from django.contrib import admin
from django.urls import path
import zendesk.views

urlpatterns = [
    path('', zendesk.views.index, name='index'),
    path('ticket/<str:ticket_id>/', zendesk.views.ticket, name='ticket'),
    path('error/', zendesk.views.error, name='error'),
    path('admin/', admin.site.urls),
]
