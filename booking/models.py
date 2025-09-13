from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  
    date = models.DateField()                                  
    time = models.TimeField()                                  
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'รอดำเนินการ'),
            ('approved', 'อนุมัติแล้ว'),
            ('rejected', 'ปฏิเสธ')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.room.name} - {self.date} {self.time}"
