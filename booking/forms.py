from django import forms
from .models import Booking, Review, Service, RoomType

class BookingForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Дополнительные услуги"
    )
    
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'services']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Дата выезда должна быть позже даты заезда!")
            
        return cleaned_data
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        
class RoomFilterForm(forms.Form):
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        required=False,
        label='Тип номера',
        empty_label='Все типы'
    )
    min_price = forms.IntegerField(
        required=False,
        label='Цена от',
        widget=forms.NumberInput(attrs={'placeholder': '₽'})
    )
    max_price = forms.IntegerField(
        required=False,
        label='Цена до',
        widget=forms.NumberInput(attrs={'placeholder': '₽'})
    )
    capacity = forms.IntegerField(
        required=False,
        label='Вместимость от',
        widget=forms.NumberInput(attrs={'placeholder': 'чел.'})
    )