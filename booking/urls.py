# booking/urls.py

from django.urls import path
from booking.views import FitnessClassListView, BookClassView, BookingListView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='classes'),
    path('book/', BookClassView.as_view(), name='book'),
    path('bookings/', BookingListView.as_view(), name='bookings'),
]
