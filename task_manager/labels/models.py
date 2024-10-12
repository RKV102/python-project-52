from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            verbose_name=_('Name'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at')
                                      )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at')
                                      )

    class Meta:
        verbose_name = _('label')
        verbose_name_plural = _('labels')

    def __str__(self):
        return self.name
