from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from .forms import BookingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .booking_services import BookingService

def home(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'booking/home.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)
    booking_service = BookingService()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_service.create_booking(room=room, user=request.user,form=form)
            messages.success(request, "Вы успешно забронировали номер!")
            return redirect('profile')
    else:
        form = BookingForm()
    return render(request, 'booking/book.html', {'form': form, 'room': room})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Вы успешно отменили бронирование!")
    return redirect('profile')

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/profile.html', {'bookings': bookings})