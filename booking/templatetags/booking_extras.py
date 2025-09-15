from django import template

register = template.Library()

@register.filter
def get_booking_for_room(bookings, room):
    for booking in bookings:
        if booking.room == room:
            return booking
    return None
