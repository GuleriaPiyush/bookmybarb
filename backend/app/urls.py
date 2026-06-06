from django.urls import path
from .views import (
    ServiceView, ServiceCreate, assign_templates_to_dates, 
    available_slots, create_booking, list_bookings, update_booking_status
)

urlpatterns = [
    # shop owner urls
    path("services/", ServiceView, name="serviceview"),
    path("services/create/", ServiceCreate, name="servicecreate"),
    path("assign-template/", assign_templates_to_dates, name="assigntemplate"),
    path("available-slots/", available_slots, name="availableslots"),
    
    # booking urls
    path("bookings/create/", create_booking, name="createbooking"),
    path("bookings/requests/", list_bookings, name="listbookings"),
    path("bookings/<int:booking_id>/status/", update_booking_status, name="updatebookingstatus"),
]
