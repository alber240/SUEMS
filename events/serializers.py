from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Event,
    StudentProfile,
    Feedback,
    PastEventPost,
    PastEventPostImage,
    PostComment,
    PostReaction
)

# ------------------ USER & PROFILE ------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'user', 'role', 'nationality',
            'department', 'faculty', 'option',
            'level', 'intake', 'student_class'
        ]

# ------------------ EVENTS ------------------

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'eligibility_criteria', 'eligibility_detail']

# ------------------ FEEDBACK ------------------

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'feedback', 'created_at']

# ------------------ POST EVENT IMAGES ------------------

class PastEventPostImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PastEventPostImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

# ------------------ POST EVENT ------------------

class PastEventPostSerializer(serializers.ModelSerializer):
    images = PastEventPostImageSerializer(many=True, read_only=True)
    document = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = PastEventPost
        fields = [
            'id', 'title', 'description', 'created_at',
            'document', 'images', 'likes_count', 'dislikes_count'
        ]

    def get_document(self, obj):
        if obj.document:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.document.url) if request else obj.document.url
        return None

    def get_likes_count(self, obj):
        return obj.reactions.filter(reaction='like').count()

    def get_dislikes_count(self, obj):
        return obj.reactions.filter(reaction='dislike').count()

# ------------------ COMMENTS ------------------

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'user', 'event_post', 'text', 'timestamp']

# ------------------ REACTIONS ------------------

class PostReactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PostReaction
        fields = ['id', 'user', 'reaction']

class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PostReaction
        fields = ['id', 'user', 'post', 'reaction']
