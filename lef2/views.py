from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lef2.models import CustomUser, Event, Booking
from lef2.forms import EventForm
from django.utils import timezone
from django.db.models import Q
import re
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Booking, Payment, Event
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Notification






# -------------------------------
# ✅ Login View
# -------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # Already logged in

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')


# -------------------------------
# ✅ Register View
# -------------------------------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if not re.fullmatch(r'\d{10}', phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, 'register.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                phone_number=phone
            )
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')

    return render(request, 'register.html')


# -------------------------------
# ✅ Logout View
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------
# ✅ Home Page
# -------------------------------
@login_required(login_url='login')
def index(request):
    all_events = Event.objects.all().order_by('-date')
    music_events = Event.objects.filter(category='music').order_by('-date')
    food_events = Event.objects.filter(category='food').order_by('-date')
    art_events = Event.objects.filter(category='art').order_by('-date')
    game_events = Event.objects.filter(category='games').order_by('-date')
    tech_events = Event.objects.filter(category='tech').order_by('-date')

    return render(request, 'index.html', {
        'all_events': all_events,
        'music_events': music_events,
        'food_events': food_events,
        'art_events': art_events,
        'game_events': game_events,
        'tech_events': tech_events,
    })


# -------------------------------
# ✅ About Page
# -------------------------------
def about(request):
    return render(request, 'about.html')


# -------------------------------
# ✅ Gallery Page
# -------------------------------
def gallery(request):
    gallery_events = Event.objects.filter(is_upcoming=False).order_by('-id')
    return render(request, 'gallery.html', {'trending_events': gallery_events})


# -------------------------------
# ✅ Event Detail Page
# -------------------------------
@login_required(login_url='login')
def eventdetail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'eventdetail.html', {'event': event})


# -------------------------------
# ✅ Profile Page
# -------------------------------
login_required(login_url='login')
def profile(request):
    user = request.user
    notifications = user.notifications.order_by('-created_at')

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Update user details
        user.full_name = full_name
        user.email = email
        user.phone = phone
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'profile.html', {'user': user, 'notifications': notifications})
# -------------------------------
# ✅ Edit Profile
# -------------------------------
@login_required(login_url='login')
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        image = request.FILES.get('profile_picture')

        if not full_name or not re.match(r'^[A-Za-z\s]+$', full_name):
            messages.error(request, "Full name must only contain letters and spaces.")
            return redirect('editprofile')

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, "Please enter a valid email address.")
            return redirect('editprofile')

        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('editprofile')

        user.first_name = full_name.split(' ')[0]
        user.last_name = ' '.join(full_name.split(' ')[1:]) if len(full_name.split()) > 1 else ''
        user.email = email
        user.phone_number = phone
        if image:
            user.profile_picture = image

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'editprofile.html', {'user': user})


# -------------------------------
# ✅ Create Event
# -------------------------------
@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user

            now = timezone.now()
            if event.date < now.date():
                messages.error(request, 'Event date cannot be in the past.')
                return redirect('/createevent/')
            if event.date == now.date() and event.start_time < now.time():
                messages.error(request, 'Start time cannot be in the past.')
                return redirect('/createevent/')

            event.is_upcoming = True
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('upcoming_events')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = EventForm()
    return render(request, 'createevent.html', {'form': form})


# -------------------------------
# ✅ Edit Event
# -------------------------------
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.created_by and not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('upcoming_events')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()

            reason = request.session.pop('edit_reason', None)
            if request.user != event.created_by and reason:
                Notification.objects.create(
                    user=event.created_by,
                    message=f"Your event '{event.title}' was edited by an admin. Reason: {reason}"
                )

            messages.success(request, "Event updated successfully!")
            return redirect('upcoming_events')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = EventForm(instance=event)

    return render(request, 'editevent.html', {'form': form, 'event': event})



# -------------------------------
# ✅ Delete Event
# -------------------------------
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.created_by and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('upcoming_events')

    if request.method == 'POST':
        reason = request.POST.get('reason')

        if request.user != event.created_by and reason:
            Notification.objects.create(
                user=event.created_by,
                message=f"Your event '{event.title}' was deleted by an admin. Reason: {reason}"
            )

        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect('upcoming_events')

    return render(request, 'deleteevent.html', {'event': event})


# -------------------------------
# ✅ Book Now (Constraints)
# -------------------------------
@login_required
def booking_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        seats = int(request.POST.get('seats', 0))
        package = request.POST.get('package')
        price_per_seat = int(request.POST.get('price_per_seat', 0))
        total_price = seats * price_per_seat

        if not seats or not package:
            messages.error(request, "Please select seats and package.")
            return redirect('book', event_id=event.id)

        # Save booking
        Booking.objects.create(
            user=request.user,
            event=event,
            seats=seats,
            package=package,
            price_per_seat=price_per_seat,
            total_price=total_price
        )
        messages.success(request, "Booking successful!")
        return redirect('payment')  # Adjust if needed

    return render(request, 'book.html', {'event': event})

# -------------------------------
# ✅ Booking History
# -------------------------------
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'bookinghistory.html', {'bookings': bookings})


# -------------------------------
# ✅ Interested Event Page
# -------------------------------
def interested_event(request):
    return render(request, 'interestedevent.html')


# -------------------------------
# ✅ Category Views
# -------------------------------
def music_concerts(request):
    events = Event.objects.filter(category='music').order_by('-id')
    return render(request, 'categories/music-concerts.html', {'events': events})

def food_fests(request):
    events = Event.objects.filter(category='food').order_by('-id')
    return render(request, 'categories/food-fests.html', {'events': events})

def art_exhibitions(request):
    events = Event.objects.filter(category='art').order_by('-id')
    return render(request, 'categories/art-exhibitions.html', {'events': events})

def game_nights(request):
    events = Event.objects.filter(category='games').order_by('-id')
    return render(request, 'categories/game-nights.html', {'events': events})

def tech_summits(request):
    events = Event.objects.filter(category='tech').order_by('-id')
    return render(request, 'categories/tech-summits.html', {'events': events})


# -------------------------------
# ✅ Upcoming Events with Role
# -------------------------------
@login_required
def upcoming_events(request):
    now = timezone.now()
    today = now.date()
    current_time = now.time()

    # Fetch upcoming events based on date and time
    upcoming_events = Event.objects.filter(
        is_upcoming=True
    ).filter(
        Q(date__gt=today) | Q(date=today, start_time__gte=current_time)
    ).order_by('date', 'start_time')

    user_role = request.user.role  # Assuming 'role' is a field in your custom user model

    return render(request, 'upcoming_events.html', {
        'upcoming_events': upcoming_events,
        'user_role': user_role,
        'current_user': request.user,
    })


# -------------------------------
# ✅ Book Page (Placeholder)
# -------------------------------


def custom_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('custom_password_reset')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)  # ✅ Correct and secure way
            user.save()
            messages.success(request, "Password successfully changed! Please login with your new password.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('custom_password_reset')

    return render(request, 'custom_password_reset.html')  # ✅ Use your actual template name

@login_required
def book_event(request, event_id):  # 👈 Receive the event ID from URL
    event = get_object_or_404(Event, id=event_id)  # ✅ Fetch the event

    if request.method == 'POST':
        seat_count = int(request.POST.get('seats'))
        package = request.POST.get('package')
        price_per_seat = float(request.POST.get('price_per_seat'))
        total_price = seat_count * price_per_seat

        # ✅ Create booking
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            seat_count=seat_count,
            package=package,
            price_per_seat=price_per_seat,
            total_price=total_price,
        )

        # ✅ Redirect to payment page with booking ID
        return redirect('payment', booking_id=booking.id)

    return render(request, 'book.html', {'event': event})




@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'GET':
        return render(request, 'payment.html', {'booking': booking})

    elif request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        payment_id = request.POST.get('payment_id')
        terms = request.POST.get('terms')

        if not terms:
            messages.error(request, "Please agree to terms and conditions.")
            return redirect('payment', booking_id=booking_id)

        Payment.objects.create(
            booking=booking,
            full_name=name,
            email=email,
            phone=phone,
            payment_method=payment_method,
            payment_id=payment_id
        )

        booking.status = 'CONFIRMED'
        booking.save()

        messages.success(request, "Payment successful and booking confirmed!")
        return redirect('bookinghistory')

def music_concerts(request):
    return render(request, 'music-concerts.html')

def food_fests(request):
    return render(request, 'food-fests.html')

def art_exhibition(request):
    return render(request, 'art-exhibition.html')

def gaming_nights(request):
    return render(request, 'gaming-nights.html')

def tech_summits(request):
    return render(request, 'tech-summits.html')

from django.shortcuts import render

def m1(request):
    return render(request, 'm1.html')

def m2(request):
    try:
        event = Event.objects.get(title="Rock Festival Concert")  # Adjust the title or use an ID
    except Event.DoesNotExist:
        event = None
    return render(request, 'm2.html', {'event': event})

def m3(request):
    return render(request, 'm3.html')

def m4(request):
    return render(request, 'm4.html')

def m5(request):
    return render(request, 'm5.html')

def m6(request):
    return render(request, 'm6.html')

def m7(request):
    return render(request, 'm7.html')

def m8(request):
    return render(request, 'm8.html')

def m9(request):
    return render(request, 'm9.html')

def m10(request):
    return render(request, 'm10.html')

def a1(request):
    return render(request, 'a1.html')

def a2(request):
    return render(request, 'a2.html')

def a3(request):
    return render(request, 'a3.html')

def a4(request):
    return render(request, 'a4.html')

def a5(request):
    return render(request, 'a5.html')

def a6(request):
    return render(request, 'a6.html')

def t1(request):
    return render(request, 't1.html')

def t2(request):
    return render(request, 't2.html')

def t3(request):
    return render(request, 't3.html')

def t4(request):
    return render(request, 't4.html')

def t5(request):
    return render(request, 't5.html')

def t6(request):
    return render(request, 't6.html')



def g1(request):
    return render(request, 'g1.html')

def g2(request):
    return render(request, 'g2.html')

def g3(request):
    return render(request, 'g3.html')

def g4(request):
    return render(request, 'g4.html')

def g5(request):
    return render(request, 'g5.html')

def g6(request):
    return render(request, 'g6.html')

def f1(request):
    return render(request, 'f1.html')

def f2(request):
    return render(request, 'f2.html')

def f3(request):
    return render(request, 'f3.html')

def f4(request):
    return render(request, 'f4.html')

def f5(request):
    return render(request, 'f5.html')

def f6(request):
    return render(request, 'f6.html')

def f7(request):
    return render(request, 'f7.html')

def f8(request):
    return render(request, 'f8.html')

def f9(request):
    return render(request, 'f9.html')

def f10(request):
    return render(request, 'f10.html')



# Check if user is superuser (admin)
def is_admin(user):
    return user.is_superuser

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admindashboard')  # ✅ Redirect to Dashboard after login
        else:
            return render(request, 'adminlogin.html', {'error': 'Invalid admin credentials'})
    
    return render(request, 'adminlogin.html')

@login_required
@user_passes_test(is_admin)
def admindashboard(request):
    return render(request, 'admindashboard.html')

@login_required
@user_passes_test(is_admin)
def adminmanageevents(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'admin/manageevents.html', {'events': events})


@user_passes_test(is_admin)
def admin_edit_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        reason = request.POST.get('reason')
        event = get_object_or_404(Event, id=event_id)

        # Example: Update event title or some fields (you can expand)
        # For demo, just add a note or update a dummy field
        event.notes = f"Edited by admin. Reason: {reason}"
        event.save()

        # Notify organizer
        Notification.objects.create(
            user=event.organizer,
            message=f"Your event '{event.title}' was edited by admin. Reason: {reason}"
        )

        messages.success(request, 'Event edited successfully.')
        return redirect('adminmanageevents')
    else:
        return redirect('adminmanageevents')

@user_passes_test(is_admin)
def admin_delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        reason = request.POST.get('reason')
        event = get_object_or_404(Event, id=event_id)


