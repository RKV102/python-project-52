from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_fixture_data,
                                get_users_login_data)


class TestDeleteStatus(TestCase):
    user_login_data = get_users_login_data()[0]
    status_data = get_fixture_data('statuses.json')[0]

    def setUp(self):
        call_command('create_users')
        call_command('create_statuses')
        self.created_status = Status.objects.last()

    def test_delete_status_by_unauthorized_user(self):
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.created_status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_status_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.created_status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status has been deleted")
        )
        response = self.client.get(reverse('statuses'))
        self.assertNotContains(response, self.created_status.name)

    def test_delete_used_status(self):
        call_command('create_labels')
        call_command('create_tasks')
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.created_status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status can't be deleted because it's used in the task")
        )
