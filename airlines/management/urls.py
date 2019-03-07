from django.conf.urls import url

from management.views import AssignFlight, SearchFlight, ReserveBookingForPassenger, CancelBookingForPassenger, \
    UserRudView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserRudView.as_view(), name='post-rud'),
    url(r'^assign_flight/$', AssignFlight.as_view(), name='assign_flight'),
    url(r'^search_flight/$', SearchFlight.as_view(), name='search_flight'),
    url(r'^passenger_booking/$', ReserveBookingForPassenger.as_view(), name='passenger_booking'),
    url(r'^cancel_passenger_booking/$', CancelBookingForPassenger.as_view(), name='cancel_passenger_booking'),
]
