# Generated by Django 4.2.3 on 2024-01-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0003_user_pfp_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='degree',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.CharField(max_length=100, null=True),
        ),
    ]