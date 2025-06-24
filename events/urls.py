from django.urls import path
from .views import EventListAPIView, register_for_event

urlpatterns = [
    path('api/events/', EventListAPIView.as_view(), name='api-events'),
    path('api/register/', register_for_event, name='register-event'),
]
