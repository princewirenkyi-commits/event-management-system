from django.contrib import admin
from .models import Event, EventAttendee
 
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display        = ['title', 'category', 'event_type', 'status', 'start_datetime', 'max_attendees']
    list_filter         = ['category', 'event_type', 'status']
    search_fields       = ['title', 'organizer_name', 'organizer_email']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page       = 20
 
@admin.register(EventAttendee)
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display  = ['event', 'attendee', 'registration_date', 'attended']
    list_filter   = ['attended']
    search_fields = ['event__title', 'attendee__first_name', 'attendee__email']
