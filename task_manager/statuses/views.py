from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from .models import Status
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from task_manager.mixins import LoginRequiredMixin


STATUSES_URL = reverse_lazy('statuses')


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


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = STATUSES_URL
    success_message = _('Status has been deleted')
