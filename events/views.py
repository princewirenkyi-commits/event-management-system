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
    category = request.GET.get('category')
    event_type = request.GET.get('eventType')
    event_status = request.GET.get('eventStatus')
    if category:
        events = Event.Objects.filter(category = category)
        
    if event_type:
        events = Event.objects.filter(event_type= event_type)
    
    if event_status:
        events = Event.objects.filter(event_status= event_status)
        
    context = {
        "category": Event.CategoryChoices,
        "event_type": Event.event_type_choices,
        "event_status": Event.status_choices,
    }
    
    return render(request, 'events/events.html',context)
    

def event_detail(request, slug):
    event_detail = get_object_or_404(Event, slug=slug)
    
    attendees = EventAttendee.object.filter(event = event)
    AttendeeNumber = attendees.count()
    Capacity = Event.max_attendees
    
    context = {
        "event_detail": event_detail,
        "atendees": attendees,
        "AttendeeNUmber": AttendeeNumber,
        "Capacity":Capacity,
        
    }
    
    return render(request, 'events/eventDetail.html',context)

def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.slug = slugify(event.title)
            event.save()

            return redirect("event_detail", slug=event.slug)

    else:
        form = EventForm()
        
    context = {
        "form": form
        }

    return render(request, "events/createEvent.html", context)


def event_edit(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if event.start_date <= timezone.now():
        messages.error(request, "You cannot edit an event that has already started.")
        return redirect("event_detail", slug=event.slug)

    form = EventForm(request.POST or None, instance=event)

    if request.method == "POST":
        if form.is_valid():
            updated_event = form.save(commit=False)
            updated_event.slug = event.slug

            updated_event.save()

            return redirect("event_detail", slug=event.slug)
        
    context = {
        "form": form,
        "event": event
    }

    return render(request, "events/editEvent.html", context )


def event_cancel(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.method == "GET":
        return render(request, "events/cancelEvent.html", {"event": event})

    if request.method == "POST":
        if event.status == "cancelled":
            messages.info(request, "Event is already cancelled.")
        else:
            event.status = "cancelled"
            event.save()
            messages.success(request, "Event cancelled successfully.")

        return redirect("event_detail", slug=event.slug)
    
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

    





    
    
