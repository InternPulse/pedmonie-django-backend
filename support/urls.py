from django.urls import path
from .views import SupportTicketListView, SupportTicketDetailView, SupportMessageCreateView

urlpatterns = [
    path("admin/support/", SupportTicketListView.as_view(), name="list-support-tickets"),
    path("admin/support/tickets/<uuid:ticket_id>", SupportTicketDetailView.as_view(), name="get-support-ticket"),
    path("admin/support/tickets/<uuid:ticket_id>/messages", SupportMessageCreateView.as_view(), name="create-support-message"),
    
]
