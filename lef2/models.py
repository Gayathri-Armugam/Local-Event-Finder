from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ------------------------
# Payment Choices (Global)
# ------------------------
PAYMENT_METHOD_CHOICES = [
    ('upi', 'UPI'),
    ('card', 'Card'),
    ('wallet', 'Wallet'),
]

# ------------------------
# Custom User Model
# ------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('organizer', 'Organizer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='attendee')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ------------------------
# Event Model
# ------------------------
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('food', 'Food'),
        ('art', 'Art'),
        ('games', 'Games'),
        ('tech', 'Tech'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', default='event_images/host.jpg')
    packages = models.TextField()
    slots = models.PositiveIntegerField()
    book_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_upcoming = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='music')

    def __str__(self):
        return self.title

    def organizer_name(self):
        return self.created_by.username

# ------------------------
# Booking Model
# ------------------------
class Booking(models.Model):
    PACKAGE_CHOICES = [
        ('LOUNGER', 'LOUNGER'),
        ('PRIME', 'PRIME'),
        ('CLASSIC', 'CLASSIC'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
    seat_count = models.PositiveIntegerField()
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    booked_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.seat_count * self.price_per_seat
        super().save(*args, **kwargs)

    def payment_status(self):
        try:
            return f"Paid via {self.payment.payment_method.upper()}"
        except Payment.DoesNotExist:
            return "Not Paid"

    def __str__(self):
        return f"{self.user.username} booked {self.seat_count} seat(s) for {self.event.title}"

# ------------------------
# Payment Model
# ------------------------
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.full_name} for booking {self.booking.id}"

# ------------------------
# Notification Model
# ------------------------
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:30]}"
