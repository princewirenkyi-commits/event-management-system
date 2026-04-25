from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.attendee_list, name='attendee_list'),
    path('register/', views.attendee_register, name='attendee_register'),
    path('<str:attendee_id>/', views.attendee_profile, name='attendee_profile'),
    path('<str:attendee_id>/edit/', views.attendee_edit, name='attendee_edit'),
    path('<str:attendee_id>/deactivate/', views.attendee_deactivate, name='attendee_deactivate'),
]
