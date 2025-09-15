from django.shortcuts import render, get_object_or_404, redirect
from .models import Room
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm
from django.contrib import messages
from .models import Booking


def home(request):
    return render(request, 'home.html')


@login_required
def rooms(request):
    rooms = Room.objects.all()
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'rooms.html', {'rooms': rooms, 'user_bookings': user_bookings})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            messages.success(request, f'จองห้อง "{room.name}" สำเร็จแล้ว!')
            return redirect('rooms')
        else:
            messages.error(request, 'กรุณากรอกข้อมูลให้ถูกต้อง')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'room': room})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


