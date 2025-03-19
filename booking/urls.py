from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:room_id>/', views.book_room, name='book'),
    path('profile/delete/<int:booking_id>', views.delete_booking, name='delete_booking'),
    path('profile/', views.profile, name='profile'),
]
