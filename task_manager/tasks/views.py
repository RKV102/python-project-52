from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from .models import Task
from .forms import TaskChangeForm, TaskCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin as
                                        DjangoLoginRequiredMixin)


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    login_url = reverse_lazy('index')
    redirect_field_name = None


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
        form = TaskCreationForm(
            initial={'creator': creator}
        )
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Creation was successful'))
            return redirect('tasks')
        return render(request, self.template_name, {'form': form})


class UpdateTaskView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskChangeForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task has been updated')


class DeleteTaskView(LoginRequiredMixin, View):
    template_name = 'tasks/delete.html'

    def get(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        task_pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_pk)
        target_user_pk = str(task.creator.pk)
        if current_user_id != target_user_pk:
            messages.error(
                request,
                _('You cannot delete a task created by another user'),
                extra_tags='danger'
            )
            return redirect('tasks')
        return render(request, self.template_name,
                      context={'task': task})

    def post(self, request, *args, **kwargs):
        current_user_id = request.session.get('_auth_user_id')
        task_pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_pk)
        target_user_pk = str(task.creator.pk)
        if current_user_id != target_user_pk:
            messages.error(
                request,
                _('You cannot delete a task created by another user'),
                extra_tags='danger'
            )
            return render(request, self.template_name,
                          context={'task': task})
        task.delete()
        messages.success(request, _('User has been deleted'))
        return redirect('tasks')
