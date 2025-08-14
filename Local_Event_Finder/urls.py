from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from lef2 import views  # Your main views
from django.contrib.auth import views as auth_views
from lef2.views import custom_password_reset


urlpatterns = [
    path('admin/', admin.site.urls),
    # Default route to login
    path('', views.login_view, name='login'),

    # Auth routes
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Main pages
    path('index/', views.index, name='index'),  # Home page after login
    path('about/', views.about, name='about'),

    path('gallery/', views.gallery, name='gallery'),

    path('createevent/', views.create_event, name='createevent'),
    path('profile/', views.profile, name='profile'),

    # ⭐ New: Event detail page (Step 1 logic)
    path('event/<int:event_id>/', views.eventdetail, name='eventdetail'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='changepassword.html'), name='changepassword'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='changepassword.html'), name='password_change_done'),
    path('profile/interestedevent/', views.interested_event, name='interestedevent'),
    path('booking-history/', views.booking_history, name='bookinghistory'),
    path('event/<int:event_id>/', views.eventdetail, name='event_detail'),
    path('music-concerts/', views.music_concerts, name='music-concerts'),
    path('food-fests/', views.food_fests, name='food_fests'),
    path('art-exhibition/', views.art_exhibition, name='art_exhibition'),
    path('gaming-nights/', views.gaming_nights, name='gaming_nights'),
    path('tech-summits/', views.tech_summits, name='tech_summits'),
    path('forgot/change-password/', views.custom_password_reset, name='custom_password_reset'),
   path('custom-admin/login/', views.adminlogin, name='adminlogin'),
    path('custom-admin/dashboard/', views.admindashboard, name='admindashboard'),
    path('admin/manage-events/', views.adminmanageevents, name='adminmanageevents'),
    path('admin-dashboard/upcoming-events/', views.upcoming_events, name='upcomingevents'),
    



   # path('music1/', views.music1, name='music1'),
    path('upcoming_events/', views.upcoming_events, name='upcoming_events'),
    path('book/<int:event_id>/', views.book_event, name='book'),
    path('edit-event/<int:event_id>/', views.edit_event, name='editevent'),
    path('delete-event/<int:event_id>/', views.delete_event, name='deleteevent'),  # ✅ Add this
    path('payment/<int:booking_id>/', views.payment_page, name='payment'),
    path('m1/', views.m1, name='m1'),
    path('m2/', views.m2, name='m2'),
    path('m3/', views.m3, name='m3'),
    path('m4/', views.m4, name='m4'),
    path('m5/', views.m5, name='m5'),
    path('m6/', views.m6, name='m6'),
    path('m7/', views.m7, name='m7'),
    path('m8/', views.m8, name='m8'),
    path('m9/', views.m9, name='m9'),
    path('m10/', views.m10, name='m10'),
    path('t1/', views.t1, name='t1'),
    path('t2/', views.t2, name='t2'),
    path('t3/', views.t3, name='t3'),
    path('t4/', views.t4, name='t4'),
    path('t5/', views.t5, name='t5'),
    path('t6/', views.t6, name='t6'),
    path('a1/', views.a1, name='a1'),
    path('a2/', views.a2, name='a2'),
    path('a3/', views.a3, name='a3'),
    path('a4/', views.a4, name='a4'),
    path('a5/', views.a5, name='a5'),
    path('a6/', views.a6, name='a6'),
    path('f1/', views.f1, name='f1'),
    path('f2/', views.f2, name='f2'),
    path('f3/', views.f3, name='f3'),
    path('f4/', views.f4, name='f4'),
    path('f5/', views.f5, name='f5'),
    path('f6/', views.f6, name='f6'),
    path('f7/', views.f7, name='f7'),
    path('f8/', views.f8, name='f8'),
    path('f9/', views.f9, name='f9'),
    path('f10/', views.f10, name='f10'),
    path('g1/', views.g1, name='g1'),
    path('g2/', views.g2, name='g2'),
    path('g3/', views.g3, name='g3'),
    path('g4/', views.g4, name='g4'),
    path('g5/', views.g5, name='g5'),
    path('g6/', views.g6, name='g6'),

]


# Static + Media files for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
