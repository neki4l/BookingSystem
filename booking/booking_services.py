import datetime

class BookingService:
    @staticmethod
    def calculate_total_price(check_in: datetime.date, check_out: datetime.date, NightPrice: int) -> int:
        days = (check_out - check_in).days
        return days * NightPrice
    
    def create_booking(self, room, user, form):
            booking = form.save(commit=False)
            booking.user = user
            booking.room = room
            booking.total_price = self.calculate_total_price(booking.check_in,
                                                             booking.check_out,
                                                             room.room_type.price)
            booking.save()
    