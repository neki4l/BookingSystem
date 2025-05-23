from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, Review, BookingService
from django.utils import timezone
from django.db import models
from .forms import BookingForm, ReviewForm, RoomFilterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

def home(request):
    rooms = Room.objects.filter(is_available=True)
    form = RoomFilterForm(request.GET or None)
    
    if form.is_valid():
        room_type = form.cleaned_data.get('room_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        capacity = form.cleaned_data.get('capacity')
        
        if room_type:
            rooms = rooms.filter(room_type=room_type)
            
        if min_price:
            rooms = rooms.filter(room_type__price__gte=min_price)
            
        if max_price:
            rooms = rooms.filter(room_type__price__lte=max_price)
            
        if capacity:
            rooms = rooms.filter(room_type__capacity__gte=capacity)
    
    paginator = Paginator(rooms, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'booking/home.html', {
        'page_obj': page_obj,
        'form': form
    })

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
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.cancel()
        messages.success(request, "Бронирование успешно отменено")
        return redirect('profile')
    
    return redirect('profile')

@login_required
def profile(request):
    now = timezone.now().date()
    all_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    for booking in all_bookings:
        booking.check_dates()
    active_bookings = all_bookings.filter(is_cancelled=False, check_out__gte=now)
    history_bookings = all_bookings.filter(
        models.Q(is_cancelled=True) | models.Q(check_out__lt=now)
    )
    
    return render(request, 'booking/profile.html', {
        'active_bookings': active_bookings,
        'history_bookings': history_bookings,
        'now': now
    })


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