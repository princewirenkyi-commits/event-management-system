from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventAttendee
from attendees.models import Attendee
from .forms import EventForm, EventRegistrationForm
from .models import Registration
from .forms import RegistrationForm
from django.utils import timezone as tz
from django.http import HttpResponse
from django.db.models import Sum, Count, Q


 
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


def book_ticket(request, slug):
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, event=event)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.event = event
            reg.save()
            messages.success(request, f'Booking confirmed! Reference: {reg.booking_reference}')
            return redirect('booking_confirmation', ref=reg.booking_reference)
    else:
        form = RegistrationForm(event=event)
    return render(request, 'events/book_ticket.html', {'form': form, 'event': event})
 
 
def booking_confirmation(request, ref):
    reg = get_object_or_404(Registration, booking_reference=ref)
    return render(request, 'events/booking_confirmation.html', {'reg': reg})
 
 
def cancel_booking(request, ref):
    reg = get_object_or_404(Registration, booking_reference=ref)
    if request.method == 'POST':
        reg.cancelled = True
        reg.cancellation_date = tz.now()
        reg.save()
        messages.warning(request, f'Booking {ref} has been cancelled.')
        return redirect('event_detail', slug=reg.event.slug)
    return render(request, 'events/cancel_booking.html', {'reg': reg})

def analytics_dashboard(request):
    from decimal import Decimal
    events = Event.objects.filter(status='Published')
    regs   = Registration.objects.filter(cancelled=False)
 
    total_revenue   = regs.filter(payment_status='Paid').aggregate(
                          total=Sum('ticket_price'))['total'] or Decimal('0')
    paid_count      = regs.filter(payment_status='Paid').count()
    pending_count   = regs.filter(payment_status='Pending').count()
    checkin_count   = regs.filter(checked_in=True).count()
    total_regs      = regs.count()
    checkin_rate    = round((checkin_count / total_regs * 100), 1) if total_regs else 0
 
    by_ticket = regs.values('ticket_type').annotate(
                    count=Count('id'), revenue=Sum('ticket_price')).order_by('-count')
    by_method = regs.values('payment_method').annotate(count=Count('id')).order_by('-count')
 
    top_events = Event.objects.annotate(
                     reg_count=Count('registrations',
                         filter=Q(registrations__cancelled=False))
                 ).order_by('-reg_count')[:5]
 
    context = {
        'total_revenue': total_revenue, 'paid_count': paid_count,
        'pending_count': pending_count, 'checkin_count': checkin_count,
        'checkin_rate': checkin_rate, 'by_ticket': by_ticket,
        'by_method': by_method, 'top_events': top_events,
    }
    return render(request, 'events/analytics.html', context)
 
 
def export_attendees_csv(request, slug):
    event = get_object_or_404(Event, slug=slug)
    regs  = Registration.objects.filter(event=event,
                cancelled=False).select_related('attendee')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{slug}-attendees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Booking Ref', 'Name', 'Email', 'Company',
                     'Ticket', 'Price', 'Payment', 'Checked In', 'Check-in Time'])
    for reg in regs:
        writer.writerow([
            reg.booking_reference,
            reg.attendee.get_full_name(),
            reg.attendee.email,
            reg.attendee.company,
            reg.ticket_type,
            reg.ticket_price,
            reg.payment_status,
            'Yes' if reg.checked_in else 'No',
            reg.check_in_time.strftime('%d/%m/%Y %H:%M') if reg.check_in_time else '',
        ])
    return response

