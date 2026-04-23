from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventAttendee
from attendees.models import Attendee
from .forms import EventForm, EventRegistrationForm
 
 
def homepage(request):
    context = {
        'total_events':    Event.objects.filter(status='Published').count(),
        'total_attendees': Attendee.objects.filter(is_active=True).count(),
        'upcoming_count':  Event.objects.filter(status='Published',
                               start_datetime__gt=timezone.now()).count(),
        'upcoming_events': Event.objects.filter(status='Published',
                               start_datetime__gt=timezone.now()
                           ).order_by('start_datetime')[:5],
    }
    return render(request, 'homepage.html', context)
