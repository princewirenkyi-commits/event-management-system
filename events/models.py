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
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CategoryChoices)
    
    
    
    
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
        
        
        


                                  
                                  
                                  
                                  
                        
                        





