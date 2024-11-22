from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            verbose_name=_('Name'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at'),
                                      null=True
                                      )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at'),
                                      null=True
                                      )

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

    def __str__(self):
        return self.name
