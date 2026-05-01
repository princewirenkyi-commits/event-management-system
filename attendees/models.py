from django.db import models
import uuid

class Attendee(models.Model):
    attendee_id = models.CharField(max_length=10, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    date_registered = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # ----- Methods -----

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    @property
    def events_registered(self):
       return self.eventattendee_set.count()

    def save(self, *args, **kwargs):
        if not self.attendee_id:
            self.attendee_id = f"ATD-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)