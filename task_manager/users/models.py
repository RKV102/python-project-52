from django.db import models


class User(models.Model):
    name = models.CharField(max_length=15)
    family = models.CharField(max_length=15)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
