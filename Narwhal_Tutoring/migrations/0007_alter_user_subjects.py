# Generated by Django 4.2.3 on 2024-01-26 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0006_timeslot_alter_user_available_tutoravailability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='tutors', to='Narwhal_Tutoring.subject'),
        ),
    ]
