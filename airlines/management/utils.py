from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK

from management.constants import ERROR_MESSAGES
from management.models import Airplane, Airport, Flight, Passenger, Booking
from management.serializers import FlightSerializer, BookingSerializer


def check_for_all_params(params, important_params):
    missing_params = []
    for important_param in important_params:
        if not params.get(important_param):
            missing_params.append(important_param)

    if missing_params:
        error_msg = ERROR_MESSAGES['MISSING_PARAMS'].format(', '.join(missing_params))
        return Response(data={'error': error_msg}, status=HTTP_400_BAD_REQUEST)


def check_for_departure_arrival(params):
    departure_id = params.get('departure_id')
    arrival_id = params.get('arrival_id')

    if not Airport.objects.filter(pk=departure_id).exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_DEPARTURE_AIRPORT'].format(departure_id)},
                        status=HTTP_400_BAD_REQUEST)

    if not Airport.objects.filter(pk=arrival_id).exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_ARRIVAL_AIRPORT'].format(arrival_id)},
                        status=HTTP_400_BAD_REQUEST)

    if departure_id == arrival_id:
        return Response(data={'error': ERROR_MESSAGES['INVALID_AIRPORT']}, status=HTTP_400_BAD_REQUEST)


def verify_assign_flight_data(params):
    """
    There has to be 6 important params
    1 ) flight number
    2 ) airplane id
    3 ) departure id
    4 ) arrival id
    5 ) departure time
    6 ) arrival time

    :param params:
    :return:
    """
    # check for all 4 params
    important_params = ['flight_number', 'airplane_id', 'departure_id', 'arrival_id', 'departure_time', 'arrival_time']
    response = check_for_all_params(params, important_params)
    if response:
        return response

    try:
        departure_time = datetime.strptime(params.get('departure_time'), "%Y-%m-%d %H:%M:%S")
        arrival_time = datetime.strptime(params.get('arrival_time'), "%Y-%m-%d %H:%M:%S")
        params['departure_time'] = departure_time
        params['arrival_time'] = arrival_time
    except ValueError:
        return Response(data={'error': ERROR_MESSAGES['INVALID_DATETIME_FORMAT']}, status=HTTP_400_BAD_REQUEST)

    response = check_for_departure_arrival(params)
    if response:
        return response

    if departure_time > arrival_time and departure_time > datetime.now() and arrival_time > datetime.now():
        return Response(data={'error': ERROR_MESSAGES['INVALID_TIME_OF_FLIGHT'].format('YYYY-MM-DD HH:MM:SS')},
                        status=HTTP_400_BAD_REQUEST)

    try:
        airplane = Airplane.objects.get(pk=params.get('airplane_id'))
        params.update({'remaining_seats': airplane.aircraft_capacity})
        clashing_flights = airplane.flights.filter(
            Q(departure_time__lte=departure_time, arrival_time__gte=departure_time) |
            Q(departure_time__lte=arrival_time, arrival_time__gte=arrival_time)).values_list('flight_number', flat=True)

        if clashing_flights:
            error_msg = ERROR_MESSAGES['AIRCRAFT_BUSY'].format(airplane.id, ', '.join(clashing_flights))
            return Response(data={'error': error_msg}, status=HTTP_400_BAD_REQUEST)

    except Airplane.DoesNotExist:
        return Response(data={'error': ERROR_MESSAGES['AIRCRAFT_NOT_FOUND'].format(params.get('airplane_id'))},
                        status=HTTP_400_BAD_REQUEST)


def assign_flight_data(params):
    """
    Most important thing is that we need to verify assign flight data first
    :param params:
    :return:
    """
    response = verify_assign_flight_data(params)
    if response:
        return response
    flight_serializer = FlightSerializer(data=params)
    if flight_serializer.is_valid():
        flight_serializer.save()
        return Response(data=flight_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=flight_serializer.errors, status=HTTP_400_BAD_REQUEST)


def verify_search_flight_data(params):
    """
    It will only verify the data and return error response if there is issue
    :param params:
    :return:
    """
    important_params = ['date', 'departure_id', 'arrival_id']
    response = check_for_all_params(params, important_params)
    if response:
        return response

    response = check_for_departure_arrival(params)
    if response:
        return response

    try:
        date = datetime.strptime(params.get('date'), "%Y-%m-%d").date()
        if date < datetime.now().date():
            return Response(data={'error': ERROR_MESSAGES['INVALID_DATE']}, status=HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response(data={'error': ERROR_MESSAGES['INVALID_DATETIME_FORMAT'].format('YYYY-MM-DD')},
                        status=HTTP_400_BAD_REQUEST)


def search_flight_data(params):
    """

    :param params:
    :return:
    """
    response = verify_search_flight_data(params)
    if response:
        return response
    start_date = datetime.strptime(params.get('date'), "%Y-%m-%d")
    end_date = start_date + timedelta(days=1)
    flight_querset = Flight.objects.filter(
        departure_id=params.get('departure_id'), arrival_id=params.get('arrival_id'), departure_time__gte=start_date,
        departure_time__lte=end_date, remaining_seats__gt=0)
    if not flight_querset.exists():
        return Response(data={'message': ERROR_MESSAGES['NO_RECORDS_FOUND']}, status=HTTP_204_NO_CONTENT)

    flight_serializer = FlightSerializer(flight_querset, many=True)
    return Response(data=flight_serializer.data, status=HTTP_200_OK)


def verify_and_book_flight_data(params):
    """

    :param params:
    :return:
    """
    important_params = ['passenger_id', 'flight_number', 'price']
    response = check_for_all_params(params, important_params)
    if response:
        return response

    passenger_id = params.get('passenger_id')
    flight_number = params.get('flight_number')

    if not Passenger.objects.filter(pk=passenger_id).exists():
        return Response(data={'error': ERROR_MESSAGES['INVALID_PASSENGER'].format(passenger_id)},
                        status=HTTP_400_BAD_REQUEST)

    try:
        flight = Flight.objects.get(pk=flight_number)
        if not flight.remaining_seats:
            return Response(data={'error': ERROR_MESSAGES['NO_SEATS_REMAINING'].format(flight_number)},
                            status=HTTP_400_BAD_REQUEST)
        if Booking.objects.filter(passenger_id=passenger_id, flight=flight).exists():
            return Response(data={'error': ERROR_MESSAGES['ALREADY_BOOKED'].format(flight_number, passenger_id)},
                            status=HTTP_400_BAD_REQUEST)

    except Flight.DoesNotExist:
        return Response(data={'error': ERROR_MESSAGES['INVALID_FLIGHT'].format(flight_number)},
                        status=HTTP_400_BAD_REQUEST)

    try:
        params['price'] = float(params.get('price'))
    except ValueError:
        return Response(data={'error': ERROR_MESSAGES['INVALID_PRICE'].format(params.get('price'))},
                        status=HTTP_400_BAD_REQUEST)

    params['price_paid'] = True
    params['flight_id'] = params.pop('flight_number')
    booking_serializer = BookingSerializer(data=params)
    if booking_serializer.is_valid():
        booking_serializer.save()
        flight.remaining_seats -= 1
        flight.save()
        return Response(data=booking_serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(data=booking_serializer.errors, status=HTTP_400_BAD_REQUEST)


def verify_and_cancel_booking_of_flight_data(params):
    """

    :param params:
    :return:
    """
    booking_id = params.get('booking_id', '')
    try:
        booking = Booking.objects.get(pk=booking_id)
        flight = booking.flight
        flight.remaining_seats -= 1
        flight.save()
        booking.delete()
        return Response(data={'message': 'Successfully cancelled booking id {}'.format(booking_id)}, status=HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response(data={'error': ERROR_MESSAGES['INVALID_BOOKING'].format(booking_id)},
                        status=HTTP_400_BAD_REQUEST)

