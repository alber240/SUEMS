from django.contrib import admin
from .models import Event, StudentProfile, Feedback, PastEventPost, PostComment, PostReaction, PastEventPostImage

admin.site.register(Event)
admin.site.register(StudentProfile)
admin.site.register(Feedback)
admin.site.register(PostComment)
admin.site.register(PostReaction)

class PastEventPostImageInline(admin.TabularInline):
    model = PastEventPostImage
    extra = 1

class PastEventPostAdmin(admin.ModelAdmin):
    inlines = [PastEventPostImageInline]

# ✅ Register only once with inline
admin.site.register(PastEventPost, PastEventPostAdmin)
