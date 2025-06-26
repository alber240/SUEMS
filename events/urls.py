from django.urls import path
from .views import (
    CustomAuthToken,
    EventListAPIView,
    register_for_event,
    submit_feedback,
    PastEventPostListAPIView,
    upload_past_event_post,
    react_to_post,
    comment_on_post,
    get_comments_for_post
)

urlpatterns = [
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
    path('api/events/', EventListAPIView.as_view(), name='event-list'),
    path('api/register/', register_for_event, name='event-register'),

    # Feedback
    path('api/feedback/', submit_feedback, name='feedback'),

    # Past Events
    path('api/past-events/', PastEventPostListAPIView.as_view(), name='past-events-list'),
    path('api/past-events/upload/', upload_past_event_post, name='past-events-upload'),

    # Reactions and Comments
    path('api/event/<int:post_id>/react/', react_to_post, name='post-react'),
    path('api/event/<int:post_id>/comment/', comment_on_post, name='post-comment'),
    path('api/event/<int:post_id>/comments/', get_comments_for_post, name='post-comments'),
]
