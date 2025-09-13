from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("ยินดีต้อนรับสู่ระบบจองห้องเรียน!")
