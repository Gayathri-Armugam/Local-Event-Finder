from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.timezone import now

from .models import CustomUser, Event, Booking, Payment


# -------------------- 1. Custom User Management --------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

# -------------------- 2. Event Management --------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer_name', 'date', 'location', 'is_upcoming', 'category')
    search_fields = ('title', 'location', 'created_by__username')
    list_filter = ('date', 'is_upcoming', 'category')
    list_editable = ('is_upcoming',)

# -------------------- 3. Booking Management --------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'seat_count', 'package', 'total_price', 'status', 'booked_at', 'payment_status_display')

    def payment_status_display(self, obj):
        return obj.payment_status()
    payment_status_display.short_description = 'Payment Status'

# -------------------- 4. Payment Management --------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'full_name', 'email', 'payment_method', 'payment_id', 'payment_date')
    search_fields = ('full_name', 'payment_id')
    list_filter = ('payment_method', 'payment_date')

# -------------------- 5. Custom Admin View: Upcoming Events --------------------
def upcomingeventsview(request):
    events = Event.objects.filter(date__gte=now()).order_by('date')
    context = dict(
        admin.site.each_context(request),
        events=events,
        title="Upcoming Events",
    )
    return TemplateResponse(request, "admin/upcomingevents.html", context)

# Inject the custom admin URL
def get_admin_urls(urls):
    def get_urls():
        custom_urls = [
            path('upcoming-events-admin/', admin.site.admin_view(upcomingeventsview), name='admin-upcoming-events'),
        ]
        return custom_urls + urls
    return get_urls

admin.site.get_urls = get_admin_urls(admin.site.get_urls())
