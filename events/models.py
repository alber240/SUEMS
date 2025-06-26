from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    ELIGIBILITY_CHOICES = [
        ('all_students', 'All Students'),
        ('international_students', 'International Students'),
        ('national_students', 'National Students'),
        ('department', 'Specific Department'),
        ('faculty', 'Specific Faculty'),
        ('option', 'Specific Option'),
        ('level', 'Specific Level'),
        ('class', 'Specific Class'),
        ('intake', 'Specific Intake'),
        ('staff', 'Staff'),
        ('administrators', 'Administrators'),
        ('guild', 'Guild Council'),
        ('all', 'All'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    eligibility_criteria = models.CharField(max_length=50, choices=ELIGIBILITY_CHOICES)
    eligibility_detail = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Additional detail for eligibility, e.g., department name, faculty, etc."
    )

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
        ('guild', 'Guild Council'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    nationality = models.CharField(max_length=50)
    department = models.CharField(max_length=100, blank=True)
    faculty = models.CharField(max_length=100, blank=True)
    option = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, blank=True)
    intake = models.CharField(max_length=50, blank=True)
    student_class = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"


class PastEventPost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to='post_event_docs/', blank=True, null=True)
    image = models.ImageField(upload_to='post_event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.event.title})"


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_post = models.ForeignKey(PastEventPost, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class PostReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    post = models.ForeignKey(PastEventPost, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('post', 'user')  # One reaction per user per post

    def __str__(self):
        return f"{self.reaction} by {self.user.username} on {self.post.title}"
