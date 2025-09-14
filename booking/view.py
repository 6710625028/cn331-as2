from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from django.utils import timezone
from django.contrib import messages

@login_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        date = request.POST.get('date')

        if Booking.objects.filter(room=room, date=date).exists():
            messages.error(request, "ห้องนี้ถูกจองไปแล้วในวันนั้น")
        else:
            Booking.objects.create(user=request.user, room=room, date=date)
            messages.success(request, "จองสำเร็จ!")
            return redirect('my_bookings')

    return render(request, 'booking/book_room.html', {'room': room})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})
