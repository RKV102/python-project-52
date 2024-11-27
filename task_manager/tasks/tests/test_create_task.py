from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestCreateTask(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_content('user_login.json')
        self.task_create_data = get_content('task_create.json')

    def test_create_task_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_create_task_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task creation was successful")
        )
