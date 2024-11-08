import django_filters
from django import forms
from .models import Task, Label
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('label'),
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('only own tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def __init__(self, data=None, queryset=None, user=None, *args,
                 **kwargs):
        self.user = user
        super().__init__(data, queryset, *args, **kwargs)

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.user)
        return queryset
