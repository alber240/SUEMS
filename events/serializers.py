from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import (
    Event,
    StudentProfile,
    Feedback,
    PastEventPost,
    PostComment,
    PostReaction
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['user', 'role', 'nationality', 'department', 'faculty', 'option', 'level', 'intake', 'student_class']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'eligibility_criteria', 'eligibility_detail']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'feedback', 'submitted_at']


class PastEventPostListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = PastEventPost.objects.all().order_by('-created_at')
        serializer = PastEventPostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class PastEventPostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    document = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = PastEventPost
        fields = ['id', 'title', 'description', 'created_at', 'image', 'document', 'likes_count', 'dislikes_count']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_document(self, obj):
        if obj.document:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.document.url) if request else obj.document.url
        return None

    def get_likes_count(self, obj):
        return obj.reactions.filter(reaction='like').count()

    def get_dislikes_count(self, obj):
        return obj.reactions.filter(reaction='dislike').count()




class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'event_post', 'text', 'timestamp']



class LikeDislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostReaction
        fields = ['id', 'user', 'event_post', 'is_like', 'timestamp']
class PostReactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PostReaction
        fields = ['id', 'user', 'reaction']
