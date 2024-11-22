from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data, create_users)


class TestReadTask(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_users_login_data()[0]
        self.task_data = get_fixture_data('tasks.json')[0]
        self.task_create_data = get_fixture_data('tasks.json')[0]

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
        response = self.client.get(reverse('tasks'))
        self.assertContains(response, self.task_data['name'])
