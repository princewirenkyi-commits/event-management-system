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
    