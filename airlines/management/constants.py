

ERROR_MESSAGES = {
    'MISSING_PARAMS': 'parameters missing {}',
    'INVALID_AIRPORT': "departure airport and arrival airport can't be the same",
    'INVALID_DATETIME_FORMAT': "the datetime format for arrival time or departure time is invalid. Desired format {}",
    'INVALID_TIME_OF_FLIGHT': "departure time should be greater than arrival time and both time shall be greater than "
                              "current time",
    'AIRCRAFT_BUSY': "For aircraft id {}, new flight is clashing with flight ids {}",
    'AIRCRAFT_NOT_FOUND': "For aircraft id {}, no such aircraft exists",
    'INVALID_DEPARTURE_AIRPORT': "airport id {} for departure doesn't exists",
    'INVALID_ARRIVAL_AIRPORT': "airport id {} for arrival doesn't exists",
    'INVALID_DATE': "date of search cannot be less than current date",
    'INVALID_PASSENGER': "no such passenger id {} exists",
    'INVALID_FLIGHT': "no such flight id {} exists",
    'INVALID_BOOKING': "no such booking id {} exists",
    'INVALID_PRICE': "invalid price {}",
    'NO_RECORDS_FOUND': "no flights found",
    'NO_SEATS_REMAINING': "no seats remaining",
    'ALREADY_BOOKED': "There is already a booking for this flight {} and passenger id {}",
}
