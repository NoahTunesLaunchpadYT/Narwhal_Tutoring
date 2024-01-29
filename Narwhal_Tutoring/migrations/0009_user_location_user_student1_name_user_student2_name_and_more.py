# Generated by Django 4.2.3 on 2024-01-28 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Narwhal_Tutoring', '0008_remove_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='student1_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='student2_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='student3_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]