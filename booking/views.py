from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, Review, BookingService
from .forms import BookingForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def home(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'booking/home.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            try:
                booking.save()
                booking.clean()
                for service in form.cleaned_data['services']:
                    BookingService.objects.create(booking=booking, service=service)
                booking.calculate_total_price()
                messages.success(request, "Вы успешно забронировали номер!")
                return redirect('profile')
            except ValidationError as e:
                messages.error(request, e.message)
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


def show_reviews(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    return render(request, 'booking/reviews.html', {'form': form, 'reviews': all_reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен!")
    return redirect('reviews')
        

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
        messages.success(request, "Ваш отзыв был удалён.")
    else:
        messages.error(request, "Вы не можете удалить этот отзыв.")
    return redirect('reviews')