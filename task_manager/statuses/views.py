from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from .models import Status
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from task_manager.mixins import LoginRequiredMixin


STATUSES_URL = reverse_lazy('statuses')


class UsageCheckMixin(AccessMixin):
    message_text = _("Status can't be deleted because it's used in the task")

    def dispatch(self, request, *args, **kwargs):
        status_id = kwargs['pk']
        status = get_object_or_404(self.model, id=status_id)
        if status.task_set.all():
            messages.error(
                request,
                self.message_text,
                extra_tags='danger'
            )
            return redirect('statuses')
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/index.html',
            context={'statuses': statuses}
        )


class CreateStatusView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses/create.html'
    success_url = STATUSES_URL
    success_message = _('Creation was successful')


class UpdateStatusView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses/update.html'
    success_url = STATUSES_URL
    success_message = _('Status has been updated')


class DeleteStatusView(LoginRequiredMixin, UsageCheckMixin,
                       SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = STATUSES_URL
    success_message = _('Status has been deleted')
