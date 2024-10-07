from django import forms
from task_manager.tasks.models import Task


class TaskMixin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'performer', 'creator')


class TaskCreationForm(TaskMixin, forms.ModelForm):
    pass


class TaskChangeForm(TaskMixin, forms.ModelForm):
    pass
