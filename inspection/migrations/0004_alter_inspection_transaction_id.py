# Generated by Django 3.2.20 on 2023-07-08 08:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0003_auto_20230707_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='transaction_id',
            field=models.UUIDField(default=uuid.UUID('70255b01-48bf-4bfa-8ba5-4bce9f9c50e1'), editable=False),
        ),
    ]
