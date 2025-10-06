from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Booking
from .forms import BookingForm, RegisterForm


def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

@login_required
def rooms(request):
    rooms = Room.objects.all()
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'rooms.html', {'rooms': rooms, 'user_bookings': user_bookings})

@login_required
def book_room(request, room_id):
    # ใช้ฟอร์ม BookingForm ในการจองห้องพักเฉพาะ
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

@login_required
def booking_form(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        # การตรวจสอบความถูกต้องควรถูกเพิ่มที่นี่ เพื่อให้ปลอดภัยยิ่งขึ้น
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        time = request.POST.get('time')
        room = Room.objects.get(id=room_id)
        Booking.objects.create(room=room, user=request.user, date=date, time=time)
        messages.success(request, 'จองห้องสำเร็จแล้ว!')
        return redirect('home')
    return render(request, 'booking_form.html', {'rooms': rooms})

def login_view(request):
    error = None 
    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    return render(request, 'login.html', {'error': error}) 


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
