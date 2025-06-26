from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    Event,
    StudentProfile,
    Feedback,
    PastEventPost,
    PostComment,
    PostReaction
)
from .serializers import (
    EventSerializer,
    FeedbackSerializer,
    PastEventPostSerializer,
    CommentSerializer,
    LikeDislikeSerializer
)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })


class EventListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_for_post(request, post_id):
    comments = PostComment.objects.filter(event_post__id=post_id).order_by('-timestamp')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_for_event(request):
    user = request.user
    event_id = request.data.get('event_id')

    try:
        event = Event.objects.get(id=event_id)
        profile = StudentProfile.objects.get(user=user)
    except (Event.DoesNotExist, StudentProfile.DoesNotExist):
        return Response({"message": "Event or profile not found."}, status=status.HTTP_404_NOT_FOUND)

    criteria = event.eligibility_criteria
    detail = event.eligibility_detail.lower() if event.eligibility_detail else None
    is_eligible = False

    # Eligibility checks:
    if criteria in ['all', 'all_students']:
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
    elif criteria == 'department' and detail:
        is_eligible = profile.department.lower() == detail
    elif criteria == 'faculty' and detail:
        is_eligible = profile.faculty.lower() == detail
    elif criteria == 'option' and detail:
        is_eligible = profile.option.lower() == detail
    elif criteria == 'level' and detail:
        is_eligible = profile.level.lower() == detail
    elif criteria == 'class' and detail:
        is_eligible = profile.student_class.lower() == detail
    elif criteria == 'intake' and detail:
        is_eligible = profile.intake.lower() == detail

    if is_eligible:
        return Response({"message": "Registration successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You are not eligible to register for this event."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Feedback submitted."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PastEventPostListAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to view past event posts

    def get(self, request):
        posts = PastEventPost.objects.all().order_by('-created_at')
        serializer = PastEventPostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_past_event_post(request):
    if not request.user.is_staff:
        return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    serializer = PastEventPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(posted_by=request.user)
        return Response({"message": "Post uploaded."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_for_post(request, post_id):
    comments = PostComment.objects.filter(event_post__id=post_id).order_by('-timestamp')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_post(request, post_id):
    post = get_object_or_404(PastEventPost, id=post_id)
    text = request.data.get("text") or request.data.get("comment")
    if not text or text.strip() == "":
        return Response({"message": "Empty comment."}, status=status.HTTP_400_BAD_REQUEST)
    
    PostComment.objects.create(user=request.user, event_post=post, text=text.strip())
    return Response({"message": "Comment submitted."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_post(request, post_id):
    post = get_object_or_404(PastEventPost, id=post_id)
    is_like = request.data.get("is_like")

    if is_like is None:
        return Response({"message": "is_like field is required."}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(is_like, bool):
        if isinstance(is_like, str):
            if is_like.lower() == 'true':
                is_like = True
            elif is_like.lower() == 'false':
                is_like = False
            else:
                return Response({"message": "Invalid value for is_like. Use true or false."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid value for is_like."}, status=status.HTTP_400_BAD_REQUEST)

    reaction, created = PostReaction.objects.get_or_create(user=request.user, post=post)
    reaction.is_like = is_like
    reaction.save()

    return Response({"message": "Reaction recorded."}, status=status.HTTP_200_OK)
