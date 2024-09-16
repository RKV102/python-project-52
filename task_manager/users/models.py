from django.db import models


class User(models.Model):
    short_name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
