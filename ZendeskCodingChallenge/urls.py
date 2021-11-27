"""ZendeskCodingChallenge URL Configuration
"""
from django.contrib import admin
from django.urls import path
import zendesk.views

urlpatterns = [
    path('', zendesk.views.index, name='index'),
    path('admin/', admin.site.urls),
]
