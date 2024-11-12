from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext_lazy as _
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from task_manager.mixins import LoginRequiredMixin
from .filters import TaskFilter
from task_manager.mixins import BaseSuccessUrlMixin


class SuccessUrlMixin(BaseSuccessUrlMixin):
    redirect_url = 'tasks'


class ModelMixin:
    model = Task


class CreatorCheckMixin(AccessMixin):
    message_text = _('Only the creator of the task can delete it')

    def dispatch(self, request, *args, **kwargs):
        current_user_id = request.user.id
        target_task_id = kwargs['pk']
        target_user_id = get_object_or_404(
            self.model,
            id=target_task_id
        ).creator.id
        if current_user_id != target_user_id:
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        filter = TaskFilter(request.GET, queryset=tasks, user=request.user)
        filtered_tasks = filter.qs if filter.is_valid() else tasks
        return render(
            request,
            'tasks/index.html',
            context={'tasks': filtered_tasks, 'filter': filter}
        )


class ShowTaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.object.labels.all()
        return context


class CreateTaskView(LoginRequiredMixin, View):
    template_name = 'tasks/create.html'

    def get(self, request, *args, **kwargs):
        creator = request.user
        form = TaskForm(
            initial={'creator': creator}
        )
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task creation was successful'))
            return redirect('tasks')
        return render(request, self.template_name, {'form': form})


class UpdateTaskView(ModelMixin, SuccessUrlMixin, LoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_message = _('Task has been updated')


class DeleteTaskView(ModelMixin, SuccessUrlMixin, LoginRequiredMixin,
                     CreatorCheckMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    success_message = _('Task has been deleted')
