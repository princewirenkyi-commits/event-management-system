from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from attendees.models import Attendee


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
        
        
        


                                  
                                  
                                  
                                  
                        
                        





