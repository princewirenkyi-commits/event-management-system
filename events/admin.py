from django.contrib import admin
from .models import Event, EventAttendee, Atendee

# Register your models here.
admin.site.register(Event)
admin.site.register(EventAttendee)
admin.site.register(Atendee)



