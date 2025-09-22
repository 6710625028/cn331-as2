from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# นำเข้า Models และ Forms ทั้งหมด
from .models import Room, Booking
from .forms import BookingForm, RegisterForm


# --- 1. Home View ---
def home(request):
    # แสดงรายการห้องทั้งหมด
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


# --- 2. Room Listing and Detail Booking ---
@login_required
def rooms(request):
    # แสดงรายการห้องและการจองของผู้ใช้ (ถ้ามี)
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


# --- 3. Simple Booking Form (ถูกผสานกับ book_room แต่ URL ยังมีอยู่) ---
@login_required
def booking_form(request):
    # ใช้ฟอร์ม BookingForm ในการจองห้อง (กรณีเรียกผ่าน URL /booking/)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'จองห้องสำเร็จแล้ว!')
            # ควรเปลี่ยนเป็น redirect ไปที่หน้าแสดงรายการห้อง
            return redirect('rooms') 
        else:
            messages.error(request, 'กรุณากรอกข้อมูลให้ถูกต้อง')
            # ดึงห้องทั้งหมดมาแสดงอีกครั้งเมื่อเกิด error
            rooms = Room.objects.all()
            return render(request, 'booking_form.html', {'rooms': rooms, 'form': form})
    else:
        # แสดงฟอร์มจอง (อาจจะดึง room list มาใช้ในฟอร์ม)
        rooms = Room.objects.all()
        form = BookingForm()
    return render(request, 'booking_form.html', {'rooms': rooms, 'form': form})


# --- 4. Authentication Views ---
def login_view(request):
    # ผสานการจัดการ POST และ messages ที่ดีที่สุด
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ใช้ 'rooms' หรือ 'home' เป็นจุด redirect หลัง login สำเร็จ
            return redirect('rooms') 
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            # ไม่ต้องส่ง 'error' ใน context เพราะใช้ messages.error แทนแล้ว
    
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