from django.db import models

# Create your models here.
class Attendee(models.Model):
    attendee_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    date_registered = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    #-----Methods------
    def __str__(self):
        return self.first_name
    
        
    def get_full_name():
        return Attendee.first_name + Attendee.last_name
    
    
        
    
    
    
