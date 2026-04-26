

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Attendee
from .forms import AttendeeForm
 
 
def attendee_list(request):
    attendees = Attendee.objects.all()
    search = request.GET.get('search', '')
    if search:
        attendees = attendees.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) |
            Q(email__icontains=search) | Q(company__icontains=search)
        )
    status = request.GET.get('status', '')
    if status == 'active':   attendees = attendees.filter(is_active=True)
    elif status == 'inactive': attendees = attendees.filter(is_active=False)
    return render(request, 'attendees/attendee_list.html',
                  {'attendees': attendees, 'search': search, 'status': status})
 
 
def attendee_profile(request, attendee_id):
    attendee = get_object_or_404(Attendee, attendee_id=attendee_id)
    from events.models import EventAttendee
    registrations = EventAttendee.objects.filter(attendee=attendee).select_related('event')
    return render(request, 'attendees/attendee_profile.html',
                  {'attendee': attendee, 'registrations': registrations})
 
 
def attendee_register(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            messages.success(request,
                f'{attendee.get_full_name()} registered! ID: {attendee.attendee_id}')
            return redirect('attendee_profile', attendee_id=attendee.attendee_id)
    else:
        form = AttendeeForm()
    return render(request, 'attendees/attendee_form.html', {'form': form, 'action': 'Register'})
 
 
def attendee_edit(request, attendee_id):
    attendee = get_object_or_404(Attendee, attendee_id=attendee_id)
    if request.method == 'POST':
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendee updated.')
            return redirect('attendee_profile', attendee_id=attendee_id)
    else:
        form = AttendeeForm(instance=attendee)
    return render(request, 'attendees/attendee_form.html',
                  {'form': form, 'action': 'Edit', 'attendee': attendee})
 
 
def attendee_deactivate(request, attendee_id):
    attendee = get_object_or_404(Attendee, attendee_id=attendee_id)
    if request.method == 'POST':
        attendee.is_active = False
        attendee.save()
        messages.warning(request, f'{attendee.get_full_name()} deactivated.')
        return redirect('attendee_list')
    return render(request, 'attendees/attendee_deactivate.html', {'attendee': attendee})

