# Generated by Django 4.1.5 on 2023-06-17 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_delete_friendrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
    ]