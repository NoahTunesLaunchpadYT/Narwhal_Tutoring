# Generated by Django 4.2.3 on 2024-01-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0015_availability_day_of_week_alter_availability_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='end_time',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='availability',
            name='start_time',
            field=models.CharField(max_length=20),
        ),
    ]
