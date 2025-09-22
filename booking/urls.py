from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # เส้นทางหลัก
    path('', views.home, name='home'),
    
    # การจัดการห้องพักและการจอง (จาก HEAD)
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    
    # ฟอร์มจองห้องพักแบบทั่วไป (จาก 21984aa) - ใช้ booking_form() ใน views.py
    path('booking/', views.booking_form, name='booking_form'),
    
    # การจัดการผู้ใช้และการเข้าสู่ระบบ
    # Login: ใช้ Django's built-in LoginView (จาก HEAD) 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Logout: ใช้ Django's built-in LogoutView (รวม next_page จาก 21984aa)
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Register: ใช้ฟังก์ชัน register_view (จาก HEAD)
    path('register/', views.register_view, name='register'),
]