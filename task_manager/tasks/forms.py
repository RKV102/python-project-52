from django import forms
from ..mixins.forms import TaskMixin


class TaskCreationForm(TaskMixin, forms.ModelForm):
    pass


class TaskChangeForm(TaskMixin, forms.ModelForm):
    pass
