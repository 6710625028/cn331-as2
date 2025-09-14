from django.shortcuts import render
from .models import Room

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})
