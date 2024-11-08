from django import forms
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()
        self.fields['labels'].widget = forms.SelectMultiple()
        self.fields['labels'].queryset = Label.objects.all()

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'creator',
                  'labels')
