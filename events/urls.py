from django.urls import path
from . import views 
 
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('events/<slug:slug>/cancel/', views.event_cancel, name='event_cancel'),
    path('events/<slug:slug>/register-attendee/', views.register_attendee, name='register_attendee'),
    path('events/<slug:slug>/unregister/<str:attendee_id>/', views.unregister_attendee, name='unregister_attendee'),
    path('events/<slug:slug>/book/', views.book_ticket, name='book_ticket'),
    path('booking/<str:ref>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/<str:ref>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('events/<slug:slug>/export-csv/', views.export_attendees_csv, name='export_csv'),
   
 
]
