from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# นำเข้า Models และ Forms ทั้งหมดจากทั้งสองฝั่ง
from .models import Room, Booking
from .forms import BookingForm, RegisterForm


# --- 1. Home View ---
def home(request):
    # ใช้เวอร์ชันที่แสดงรายการห้องจาก 21984aa
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


# --- 2. Room Listing and Detail Booking (จาก HEAD) ---
@login_required
def rooms(request):
    # ใช้ 'rooms.html' เป็นเทมเพลต และดึงข้อมูลการจองของผู้ใช้มาแสดง
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


# --- 3. Simple Booking Form (จาก 21984aa) ---
@login_required
def booking_form(request):
    # ใช้สำหรับ URL: /booking/ ที่รับค่าผ่าน POST โดยไม่มี Form
    rooms = Room.objects.all()
    if request.method == 'POST':
        # การตรวจสอบความถูกต้องควรถูกเพิ่มที่นี่ เพื่อให้ปลอดภัยยิ่งขึ้น
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        time = request.POST.get('time')
        room = Room.objects.get(id=room_id)
        Booking.objects.create(room=room, user=request.user, date=date, time=time)
        messages.success(request, 'จองห้องสำเร็จแล้ว!') # เพิ่ม messages
        return redirect('home')
    return render(request, 'booking_form.html', {'rooms': rooms})


# --- 4. Authentication Views ---
def login_view(request):
    error = None # เก็บตัวแปร error จาก 21984aa
    if request.method == "POST":
        username = request.POST.get('username') # ใช้ .get() เพื่อความปลอดภัย
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # รวมการแจ้งเตือน error จากทั้งสองฝั่ง
            messages.error(request, 'Invalid username or password')
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    
    # ใช้เทมเพลตที่ถูกส่งมาจาก login.html (ควรเป็น 'login.html' หรือ 'booking/login.html' ตามที่คุณตั้งค่า)
    return render(request, 'login.html', {'error': error}) 


def register_view(request):
    # ฟังก์ชันสมัครสมาชิกจาก HEAD
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})