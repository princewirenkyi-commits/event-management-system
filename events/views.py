from django.shortcuts import render
from .models import Event, EventAttendee, Attendee
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.utils.text import slugify
from django.contrib import messages


def Events(request):
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
    

def EventDetail(request, slug):
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

def createEvent(request):
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


def edit_event(request, slug):
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


def cancelEvent(request, slug):
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
    





    
    
