import os

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Airplane(models.Model):
    type = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    aircraft_capacity = models.IntegerField(default=0)

    def __str__(self):
        return 'Aircraft {} of company {}'.format(self.type, self.company)


class Airport(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


GENDER = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
)


class Passenger(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo_path = models.ImageField(upload_to='images/', default=os.path.join(settings.BASE_DIR, 'images/xrSh9Z0.jpg'))
    cell_phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=15, choices=GENDER)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Flight(models.Model):
    flight_number = models.CharField(max_length=255, primary_key=True)
    airplane = models.ForeignKey(Airplane, related_name='flights', on_delete=models.CASCADE)
    departure = models.ForeignKey(Airport, related_name='departure_flights', on_delete=models.CASCADE)
    arrival = models.ForeignKey(Airport, related_name='arrival_flights', on_delete=models.CASCADE)
    departure_time = models.DateTimeField(null=False)
    arrival_time = models.DateTimeField(null=False)
    remaining_seats = models.IntegerField(default=0)

    def __str__(self):
        return 'Flight number {} from {} to {}'.format(self.flight_number, self.departure, self.arrival)


class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, related_name='bookings', on_delete=models.CASCADE)
    date_of_booking = models.DateTimeField(auto_now_add=True)
    flight = models.ForeignKey(Flight, related_name='flights', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    price_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('passenger', 'flight',)
