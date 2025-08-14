from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'date',
            'start_time',
            'end_time',
            'location',
            'image',
            'packages',  # Example: {'CLASSIC': 100, 'PRIME': 200}
            'slots',
            'book_url'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'packages': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Format: CLASSIC:100, PRIME:200'}),
            'slots': forms.NumberInput(attrs={'class': 'form-control'}),
            'book_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Event Title',
            'description': 'Event Description',
            'date': 'Event Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'location': 'Location',
            'image': 'Event Banner',
            'packages': 'Package & Price Details',
            'slots': 'Available Slots',
            'book_url': 'Booking URL (optional)',
        }
