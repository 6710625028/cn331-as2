from django.shortcuts import get_object_or_404, redirect
from .forms import BookingForm
from .models import Room, Booking
from django.contrib.auth.decorators import login_required

@login_required  # ถ้าต้องการให้ล็อกอินก่อนจอง
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user  # บันทึกผู้ใช้ที่จอง
            booking.save()
            return redirect('room_list')  # หรือหน้าแสดงผลสำเร็จ
    else:
        form = BookingForm()
    return render(request, 'booking/book_room.html', {'form': form, 'room': room})
