from django.contrib.auth.models import User
from rest_framework import serializers

from management.models import Passenger, Booking, Flight


class UserSerializer(serializers.ModelSerializer): # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.user.get_api_url(request=request)

    def validate_title(self, value):
        qs = User.objects.filter(username=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This username has already been taken")
        return value


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger


class BookingSerializer(serializers.ModelSerializer):
    passenger_id = serializers.IntegerField(required=True)
    flight_id = serializers.CharField(required=True, max_length=256)
    price = serializers.FloatField(required=True)
    price_paid = serializers.BooleanField(required=True)

    class Meta:
        model = Booking
        fields = ['passenger_id', 'flight_id', 'price', 'price_paid']

    # def create(self, validated_data):
    #     validated_data['flight_id'] = validated_data.pop('flight_number')
    #     return Booking.objects.create(**validated_data)


class FlightSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(required=True, max_length=256)
    airplane_id = serializers.IntegerField(required=True)
    arrival_id = serializers.CharField(required=True, max_length=256)
    departure_id = serializers.CharField(required=True, max_length=256)
    departure_time = serializers.DateTimeField(required=True)
    arrival_time = serializers.DateTimeField(required=True)
    remaining_seats = serializers.IntegerField(required=True)

    class Meta:
        model = Flight
        fields = ['flight_number', 'departure_time', 'arrival_time', 'remaining_seats', 'airplane_id', 'arrival_id',
                  'departure_id']
