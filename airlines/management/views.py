from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from management.serializers import UserSerializer
from management.utils import assign_flight_data, search_flight_data, verify_and_cancel_booking_of_flight_data, \
    verify_and_book_flight_data


class UserRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class AssignFlight(APIView):
    def post(self, request):
        return assign_flight_data(request.data)


class SearchFlight(APIView):
    def post(self, request):
        return search_flight_data(request.data)


class ReserveBookingForPassenger(APIView):
    def post(self, request):
        return verify_and_book_flight_data(request.data)


class CancelBookingForPassenger(APIView):
    def post(self, request):
        return verify_and_cancel_booking_of_flight_data(request.data)


