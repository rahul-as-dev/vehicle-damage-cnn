import uuid
from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    transaction_id = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    extension = models.CharField(max_length=100)
    image_key = models.CharField(max_length=100)
    etag = models.CharField(max_length=100)


class Inspection(models.Model):
    transaction_id = models.UUIDField(editable=False, default=uuid.uuid4())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Inspection')
    engineNumber = models.CharField(max_length=100)
    chassisNumber = models.CharField(max_length=100)
    registrationNumber = models.CharField(max_length=10)
    latitude = models.CharField(max_length=100,null=True)
    longitude = models.CharField(max_length=100,null=True)
