from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=20, unique=True)
    updated_at = models.DateTimeField(
        _("Update date"), auto_now=True
    )
    created_at = models.DateTimeField(
        _("Created date"), auto_now_add=True
    )
