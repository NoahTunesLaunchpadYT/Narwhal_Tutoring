# Generated by Django 4.2.3 on 2024-01-26 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0007_alter_user_subjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
    ]