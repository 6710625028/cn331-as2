from django.urls import path
from . import views
<<<<<<< HEAD
from django.contrib.auth import views as auth_views 
=======
from django.contrib.auth import views as auth_views

>>>>>>> c433bad (Save local changes before merge)

urlpatterns = [
    path('', views.home, name='home'),
<<<<<<< HEAD
<<<<<<< HEAD

    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('booking/', views.booking_form, name='booking_form'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
=======
    
    # การจัดการห้องพักและการจอง (จาก HEAD)
=======
>>>>>>> 18ebe60 (Update URL patterns: added auth views and register route)
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('booking/', views.booking_form, name='booking_form'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
<<<<<<< HEAD
    # Register: ใช้ฟังก์ชัน register_view (จาก HEAD)
>>>>>>> c433bad (Save local changes before merge)
=======
>>>>>>> 18ebe60 (Update URL patterns: added auth views and register route)
    path('register/', views.register_view, name='register'),
]