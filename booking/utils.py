import datetime
def TotalBookingPrice(check_in: datetime.date, check_out: datetime.date, NightPrice: int) -> int:
    days = (check_out - check_in).days
    return days * NightPrice