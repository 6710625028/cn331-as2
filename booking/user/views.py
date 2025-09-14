from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, ’home.html‘)

@login_required
def my_bookings(request):
    return HttpResponse(”นี่คือหน้าการจองของฉัน (เฉพาะผู้ที่ login แล้ว)“)


