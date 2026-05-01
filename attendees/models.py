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

    event = models.ForeignKey(
    'events.Event',
    on_delete=models.CASCADE,
    related_name='attendees',
    null=True,
    blank=True
)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def save(self, *args, **kwargs):
        if not self.attendee_id:
            self.attendee_id = f"ATD-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)