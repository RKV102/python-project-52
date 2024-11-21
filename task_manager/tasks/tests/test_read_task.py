from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data)


class TestReadTask(TestCase):
    user_login_data = get_users_login_data()[0]
    task_data = get_fixture_data('tasks.json')[0]
    task_create_data = get_fixture_data('tasks.json')[0]

    def setUp(self):
        call_command('create_users')
        call_command('create_labels')
        call_command('create_statuses')

    def test_read_task_by_unauthorized_user(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_read_task_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data,
            follow=True
        )
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, self.task_data['name'])
