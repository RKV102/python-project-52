from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import gettext as _
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib import messages
from task_manager.mixins import LoginRequiredMixin


class CreatorCheckMixin(AccessMixin):
    message_text = _('Only the creator of the task can delete it')

    def dispatch(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        current_task_id = kwargs['pk']
        target_user_id = str(
            get_object_or_404(
                self.model,
                id=current_task_id
            ).creator.id
        )
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
        return render(
            request,
            'tasks/index.html',
            context={'tasks': tasks}
        )


class CreateTaskView(LoginRequiredMixin, View):
    template_name = 'tasks/create.html'

    def get(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        creator = User.objects.get(id=current_user_id)
        form = TaskForm(
            initial={'creator': creator}
        )
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Creation was successful'))
            return redirect('tasks')
        return render(request, self.template_name, {'form': form})


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task has been updated')


class DeleteTaskView(LoginRequiredMixin, CreatorCheckMixin,
                     SuccessMessageMixin, DeleteView):
    permission_required = None
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task has been deleted')
