from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from attendees.models import Attendee
import uuid
import string, random
from django.db import models



# Create your models here.
class Event(models.Model):
    
    CategoryChoices = [
        ("Conference","conference"),
        ("Workshop","workshop"), 
        ("Webinar","webinar"), 
        ("Networking","networking"), 
        ("Seminar","seminar")
        ]
    event_type_choices = [("In-Person","in-Person"),
                          ("Virtual","virtual"),
                          ("Hybrid", "hybrid"),
                          ]
    status_choices = [("Draft","draft"),
                          ("Published","published"),
                          ("Cancelled", "cancelled"),
                          ("Completed","completed")
                          ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(max_length= 500)
    category = models.CharField(max_length=50, choices=CategoryChoices)
    capacity = models.IntegerField(default= 100)
    event_type =models.CharField(max_length=20, choices= event_type_choices)
    organizer_name =models.CharField(max_length=200)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=15)
    venue_name =models.CharField(max_length=200, blank=True)
    venue_address= models.TextField(blank=True)
    meeting_link =models.URLField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime=models.DateTimeField()
    max_attendees= models.IntegerField()
    banner_image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices= status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
      return self.title

    def save(self, *args, **kwargs):
     if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Event.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
     super().save(*args, **kwargs)

    def is_upcoming(self):
        return self.start_datetime > timezone.now()
    
    def available_slots(self):
        return self.capacity - self.attendees.count()

    class Meta:
         ordering = ['start_datetime']

    

    
    
    
    
class EventAttendee(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default= False)
    notes = models.TextField(blank=True)
        
    class Meta:
        unique_together = ['event', 'attendee']
            
        
    def __str__(self):
        return str(self.attendee)
        

class Registration(models.Model):
    TICKET_CHOICES = [
        ('General', 'General'), ('VIP', 'VIP'), ('Early Bird', 'Early Bird'),
        ('Student', 'Student'), ('Free', 'Free'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'), ('Paid', 'Paid'),
        ('Refunded', 'Refunded'), ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'), ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'), ('Cash', 'Cash'), ('Free', 'Free'),
    ]
 
    event            = models.ForeignKey(Event, on_delete=models.CASCADE,
                           related_name='registrations')
    attendee         = models.ForeignKey('attendees.Attendee', on_delete=models.CASCADE,
                           related_name='registrations')
    ticket_type      = models.CharField(max_length=20, choices=TICKET_CHOICES, default='General')
    ticket_price     = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status   = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method   = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='Free')
    transaction_id   = models.CharField(max_length=100, blank=True)
    booking_reference = models.CharField(max_length=15, unique=True, blank=True)
    checked_in       = models.BooleanField(default=False)
    check_in_time    = models.DateTimeField(null=True, blank=True)
    notes            = models.TextField(blank=True)
    cancelled        = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
 
    def generate_booking_reference(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            ref = 'BK-' + ''.join(random.choices(chars, k=8))
            if not Registration.objects.filter(booking_reference=ref).exists():
                return ref
 
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        super().save(*args, **kwargs)
 
    def is_valid(self):
        return not self.cancelled and self.payment_status in ('Paid', 'Free')
 
    def can_check_in(self):
        return self.is_valid() and not self.checked_in
 
    def __str__(self):
        return f'{self.booking_reference} — {self.attendee} @ {self.event}'
 
    class Meta:
        unique_together = ['event', 'attendee']

        
        


                                  
                                  
                                  
                                  
                        
                        





