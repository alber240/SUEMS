from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    eligibility_criteria = models.CharField(
        max_length=100,
        choices=[
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
            ('all', 'All')
        ],
        default='all',
    )

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
        ('guild', 'Guild Council'),
    ])
    nationality = models.CharField(max_length=50)  # e.g. 'Rwandan', 'International'
    department = models.CharField(max_length=100, blank=True)
    faculty = models.CharField(max_length=100, blank=True)
    option = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, blank=True)
    intake = models.CharField(max_length=50, blank=True)
    student_class = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
