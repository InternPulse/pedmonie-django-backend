from django.urls import path
from .views import SupportTicketListView, SupportTicketDetailView, SupportMessageCreateView



urlpatterns = [
    path(
        "merchants/support/tickets/",
        SupportTicketListView.as_view(),
        name="list-support-tickets",
    ),
    path(
        "merchants/support/tickets/<uuid:ticket_id>/",
        SupportTicketDetailView.as_view(),
        name="get-support-ticket",
    ),
    path(
        "merchants/support/tickets/<uuid:ticket_id>/messages",
        SupportMessageCreateView.as_view(),
        name="create-support-message",
    ),
    path(
        "admins/support/tickets",
        SupportTicketListView.as_view(),
        name="list-support-tickets",
    ),
    path(
        "admins/support/tickets/<uuid:ticket_id>",
        SupportTicketDetailView.as_view(),
        name="get-support-ticket",
    ),
    path(
        "admins/support/tickets/<uuid:ticket_id>/messages",
        SupportMessageCreateView.as_view(),
        name="create-support-message",
    ),
]