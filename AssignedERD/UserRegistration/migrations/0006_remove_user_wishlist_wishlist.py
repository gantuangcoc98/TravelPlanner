# Generated by Django 5.0 on 2024-01-01 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistration', '0005_bookorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wishlist',
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('destination_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserRegistration.destination')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserRegistration.user')),
            ],
        ),
    ]
