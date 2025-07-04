# Generated by Django 5.2.3 on 2025-06-24 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_eligibility_criteria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eligibility_criteria',
            field=models.CharField(choices=[('all_students', 'All Students'), ('international_students', 'International Students'), ('national_students', 'National Students'), ('department', 'Specific Department'), ('faculty', 'Specific Faculty'), ('option', 'Specific Option'), ('level', 'Specific Level'), ('class', 'Specific Class'), ('intake', 'Specific Intake'), ('staff', 'Staff'), ('administrators', 'Administrators'), ('guild', 'Guild Council'), ('all', 'All')], default='all', max_length=100),
        ),
    ]
