# Generated by Django 4.2.3 on 2024-01-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0004_user_address_user_degree_user_mobile_user_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(related_name='tutors', to='Narwhal_Tutoring.subject'),
        ),
    ]
