import django_filters
from .models import Task, Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('label'),
    )

    class Meta:
        model = Task
        fields = ['status', 'performer']
