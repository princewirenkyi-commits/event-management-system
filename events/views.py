from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventAttendee
from attendees.models import Attendee
from .forms import EventForm, EventRegistrationForm
 
 
def home(request):
    context = {
        'total_events':    Event.objects.filter(status='Published').count(),
        'total_attendees': Attendee.objects.filter(is_active=True).count(),
        'upcoming_count':  Event.objects.filter(status='Published',
                               start_datetime__gt=timezone.now()).count(),
        'upcoming_events': Event.objects.filter(status='Published',
                               start_datetime__gt=timezone.now()
                           ).order_by('start_datetime')[:5],
    }
    return render(request, 'home.html', context)
 
 
def event_list(request):
    events = Event.objects.all()
    search = request.GET.get('search', '')
    if search: events = events.filter(title__icontains=search)
    category = request.GET.get('category', '')
    if category: events = events.filter(category=category)
    event_type = request.GET.get('event_type', '')
    if event_type: events = events.filter(event_type=event_type)
    status = request.GET.get('status', '')
    if status: events = events.filter(status=status)
    return render(request, 'events/event_list.html',
                  {'events': events, 'search': search, 'category': category,
                   'event_type': event_type, 'status': status})
 
 
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    registrations = EventAttendee.objects.filter(event=event).select_related('attendee')
    return render(request, 'events/event_detail.html',
                  {'event': event, 'registrations': registrations})
 
 
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" created!')
            return redirect('event_detail', slug=event.slug)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})
 
 
def event_edit(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if event.start_datetime <= timezone.now():
        messages.error(request, 'Cannot edit an event that has already started.')
        return redirect('event_detail', slug=slug)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated!')
            return redirect('event_detail', slug=slug)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html',
                  {'form': form, 'action': 'Edit', 'event': event})
 
 
def event_cancel(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        event.status = 'Cancelled'
        event.save()
        messages.warning(request, f'Event "{event.title}" cancelled.')
        return redirect('event_list')
    return render(request, 'events/event_cancel.html', {'event': event})
 
 
def register_attendee(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, event=event)
        if form.is_valid():
            attendee = form.cleaned_data['attendee']
            notes    = form.cleaned_data['notes']
            EventAttendee.objects.create(event=event, attendee=attendee, notes=notes)
            messages.success(request, f'{attendee.get_full_name()} registered!')
            return redirect('event_detail', slug=slug)
    else:
        form = EventRegistrationForm(event=event)
    return render(request, 'events/register_attendee.html', {'form': form, 'event': event})
 
 
def unregister_attendee(request, slug, attendee_id):
    event    = get_object_or_404(Event, slug=slug)
    attendee = get_object_or_404(Attendee, attendee_id=attendee_id)
    reg      = get_object_or_404(EventAttendee, event=event, attendee=attendee)
    if request.method == 'POST':
        reg.delete()
        messages.success(request, f'{attendee.get_full_name()} unregistered.')
        return redirect('event_detail', slug=slug)
    return render(request, 'events/unregister_confirm.html',
                  {'event': event, 'attendee': attendee})
