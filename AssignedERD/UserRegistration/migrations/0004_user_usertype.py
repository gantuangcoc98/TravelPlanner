# Generated by Django 4.2.6 on 2023-12-20 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistration', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.IntegerField(choices=[(0, 'User'), (1, 'Admin')], default=0),
        ),
    ]
