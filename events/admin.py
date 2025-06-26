from django.contrib import admin
from .models import Event, StudentProfile, Feedback, PastEventPost, PostComment, PostReaction

admin.site.register(Event)
admin.site.register(StudentProfile)
admin.site.register(Feedback)
admin.site.register(PastEventPost)
admin.site.register(PostComment)
admin.site.register(PostReaction)
