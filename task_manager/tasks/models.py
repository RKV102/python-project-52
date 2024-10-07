from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=25, unique=True,
                            verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'), blank=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT,
                               verbose_name=_('Status'))
    creator = models.ForeignKey(User, on_delete=models.RESTRICT,
                                related_name='task_creator',
                                verbose_name=_('Creator'))
    performer = models.ForeignKey(User, on_delete=models.RESTRICT,
                                  related_name='task_performer',
                                  verbose_name=_('Performer'), blank=True,
                                  null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated at')
                                      )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created at')
                                      )

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.name