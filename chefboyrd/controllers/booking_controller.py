'''This module and its functions handle the logic for table reservations for the restaurant.
It also handles moving data in and out of our database via the via our application models.'''

from datetime import timedelta, datetime
from chefboyrd.models.tables import Table, Booking, Restaurant

def book_restaurant_table(restaurant, booking_date_time, people, name, phone, minutes_slot=90):
    """
    This method uses get_first_table_available to get the first table available, then it
    creates a Booking on the database.

    Args:
    restaurant: The id of the restaurant we want to make the booking for
    booking_time_date: The starting time of the booking we want to make
    people: The number of people that the booking is requesting
    name: The name of the guest making the reservation
    phone: The phone number of the guest making the reservation
    minutes_slot: The amount of time that the reservation is made for. Default is 90 minutes

    Returns: A dictionary with the booking id, and the table id. If there is no table available at the requested time None is returned.

    """
    table = get_first_table_available(restaurant, booking_date_time, people, minutes_slot)

    if table:
        delta = timedelta(seconds=60*minutes_slot)
        booking = Booking(table=table, people=people,
            booking_date_time_start=booking_date_time, booking_date_time_end=booking_date_time + delta, name=name, phone=phone)
        booking.save()
        return {'booking': booking.id, 'table': table.id}
    else:
        return None

def get_first_table_available(restaurant, booking_date_time, people, minutes_slot=90):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.

    Args:
    restaurant: The id of the restaurant we want to make the booking for
    booking_time_date: The starting time of the booking we want to make
    people: The number of people that the booking is requesting
    minutes_slot: The amount of time that the reservation is made for. Default is 90 minutes

    Returns: The first table available. If there are no tables available we return None
    """
    # I make sure to check if the tables are not already booked within the time slot required
    # by the new booking
    delta = timedelta(seconds=60*minutes_slot)
    l_bound_time = booking_date_time
    u_bound_time = booking_date_time + delta

    tables_booked_ids = []
    # Exclude tables which start and end booking date includes requested initial booking date_time
    for book in Booking.select().where(Booking.booking_date_time_start <= l_bound_time,Booking.booking_date_time_end >= l_bound_time):
    	tables_booked_ids.append(book.table.id)
    # Exclude tables which start and end booking date includes requested ending booking date_time
    for book in Booking.select().where(Booking.booking_date_time_start <= u_bound_time,Booking.booking_date_time_end >= u_bound_time):
    	tables_booked_ids.append(book.table.id)
    # Exclude tables which booking slots is inside requested booking slot
    for book in Booking.select().where(Booking.booking_date_time_start >= l_bound_time,Booking.booking_date_time_end <= u_bound_time):
    	tables_booked_ids.append(book.table.id)


    # Exclude tables which include requested booking slot
    for book in Booking.select().where(Booking.booking_date_time_start <= l_bound_time,Booking.booking_date_time_end >= u_bound_time):
    	tables_booked_ids.append(book.table.id)
    # Then I get a list of all the tables, of the needed size, available in that restaurant and
    # I exclude the previous list of unavailable tables. I order the list from the smaller table
    # to the bigger one and I return the first, smaller one, available.
    for table in Table.select().where(Table.size >= people).order_by(Table.size):
    	if table.restaurant.opening_time <= booking_date_time.hour and table.restaurant.closing_time >= booking_date_time.hour+(minutes_slot / float(60)):
	    	if table.id not in tables_booked_ids:
	    		return table
    return None
