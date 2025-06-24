from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Event, StudentProfile
from .serializers import EventSerializer

# Homepage view
def home(request):
    return HttpResponse("Hello, this is the SUEMS homepage!")

# Event list API
class EventListAPIView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

# Event registration with eligibility check
@api_view(['POST'])
def register_for_event(request):
    user_id = request.data.get('user_id')
    event_id = request.data.get('event_id')

    try:
        user = User.objects.get(id=user_id)
        event = Event.objects.get(id=event_id)
        profile = StudentProfile.objects.get(user=user)
    except (User.DoesNotExist, Event.DoesNotExist, StudentProfile.DoesNotExist):
        return Response({"message": "User or event not found."}, status=status.HTTP_404_NOT_FOUND)

    # Eligibility logic
    criteria = event.eligibility_criteria
    is_eligible = False

    if criteria == 'all' or criteria == 'all_students':
        is_eligible = profile.role == 'student'
    elif criteria == 'international_students':
        is_eligible = profile.nationality.lower() != 'rwandan'
    elif criteria == 'national_students':
        is_eligible = profile.nationality.lower() == 'rwandan'
    elif criteria == 'staff':
        is_eligible = profile.role == 'staff'
    elif criteria == 'administrators':
        is_eligible = profile.role == 'admin'
    elif criteria == 'guild':
        is_eligible = profile.role == 'guild'
    elif criteria == 'department':
        is_eligible = profile.department.lower() == 'target department'  # Replace with actual logic
    # Add additional checks for faculty, option, level, class, intake as needed

    if is_eligible:
        return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You are not eligible to register for this event."}, status=status.HTTP_403_FORBIDDEN)
# 