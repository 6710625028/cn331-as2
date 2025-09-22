from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Room, Booking

def home(request):
    rooms = Room.objects.all()
    return render(request, 'booking/home.html', {'rooms': rooms})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    return render(request, 'booking/login.html', {'error': error})

@login_required
def booking_form(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        time = request.POST.get('time')
        room = Room.objects.get(id=room_id)
        Booking.objects.create(room=room, user=request.user, date=date, time=time)
        return redirect('home')
    return render(request, 'booking/booking_form.html', {'rooms': rooms})