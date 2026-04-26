from django.contrib import admin
from .models import Attendee
 
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display  = ['attendee_id', 'first_name', 'last_name', 'email',
                     'company', 'is_active', 'date_registered']
    list_filter   = ['is_active', 'date_registered']
    search_fields = ['first_name', 'last_name', 'email', 'company', 'attendee_id']
    list_per_page = 20

