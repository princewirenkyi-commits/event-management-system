from django import forms
from django.utils.text import slugify
from .models import Event, EventAttendee
from attendees.models import Attendee
 
class EventForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = ['title','description','category','event_type','organizer_name',
                  'organizer_email','organizer_phone','venue_name','venue_address',
                  'meeting_link','start_datetime','end_datetime','max_attendees',
                  'banner_image_url','status']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description':    forms.Textarea(attrs={'rows': 5}),
        }
 
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_datetime')
        end   = cleaned_data.get('end_datetime')
        etype = cleaned_data.get('event_type')
        venue = cleaned_data.get('venue_name')
        link  = cleaned_data.get('meeting_link')
        mx    = cleaned_data.get('max_attendees')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        if mx is not None and mx <= 0:
            raise forms.ValidationError('Max attendees must be greater than 0.')
        if etype == 'In-Person' and not venue:
            raise forms.ValidationError('Venue name required for in-person events.')
        if etype == 'Virtual' and not link:
            raise forms.ValidationError('Meeting link required for virtual events.')
        return cleaned_data
 
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit: instance.save()
        return instance
 
 
class EventRegistrationForm(forms.Form):
    attendee = forms.ModelChoiceField(
        queryset=Attendee.objects.filter(is_active=True),
        empty_label='-- Select Attendee --'
    )
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
 
    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
 
    def clean(self):
        cleaned_data = super().clean()
        attendee = cleaned_data.get('attendee')
        if self.event and self.event.available_slots() <= 0:
            raise forms.ValidationError('This event is full.')
        if attendee and self.event:
            if EventAttendee.objects.filter(event=self.event, attendee=attendee).exists():
                raise forms.ValidationError('Attendee is already registered.')
        return cleaned_data
