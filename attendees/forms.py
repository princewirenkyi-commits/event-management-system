from django import forms
from .models import Attendee
 
class AttendeeForm(forms.ModelForm):
    class Meta:
        model  = Attendee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company', 'job_title']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Attendee.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('An attendee with this email already exists.')
        return email
