from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                create_users, get_fixture_data)


class TestDeleteStatus(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        create_users()
        self.created_status = Status.objects.last()
        self.user_login_data = get_users_login_data()[0]

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
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        tasks_create_data = get_fixture_data('tasks.json')
        for task_create_data in tasks_create_data:
            self.client.post(
                reverse('tasks_create'),
                data=task_create_data
            )
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.created_status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status can't be deleted because it's used in the task")
        )
