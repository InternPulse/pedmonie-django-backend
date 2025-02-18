from django.urls import path
from .views import (
    SupportTicketListView,
    SupportTicketDetailView,
    SupportMessageCreateView,
)

urlpatterns = [
    path(
        "merchants/tickets",
        SupportTicketListView.as_view(),
        name="list-support-tickets",
    ),
    path(
        "merchants/tickets/<uuid:ticket_id>",
        SupportTicketDetailView.as_view(),
        name="get-support-ticket",
    ),
    path(
        "merchants/tickets/<uuid:ticket_id>/messages",
        SupportMessageCreateView.as_view(),
        name="create-support-message",
    ),
    path(
        "admins/tickets",
        SupportTicketListView.as_view(),
        name="list-support-tickets",
    ),
    path(
        "admins/tickets/<uuid:ticket_id>",
        SupportTicketDetailView.as_view(),
        name="get-support-ticket",
    ),
    path(
        "admins/tickets/<uuid:ticket_id>/messages",
        SupportMessageCreateView.as_view(),
        name="create-support-message",
    ),
]
