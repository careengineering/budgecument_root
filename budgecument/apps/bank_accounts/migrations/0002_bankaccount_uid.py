# Generated by Django 5.0.6 on 2024-06-21 15:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank_accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="uid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
