from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('events/<slug:slug>/cancel/', views.event_cancel, name='event_cancel'),
    path('events/<slug:slug>/register-attendee/', views.register_attendee, name='register_attendee'),
    path('events/<slug:slug>/unregister/<str:attendee_id>/', views.unregister_attendee, name='unregister_attendee'),
]
