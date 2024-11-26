from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users


class TestCreateTask(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.status = Status.objects.last()
        self.user_login_data = {
            'username': self.user.username,
            'password': 'PsWd123*'
        }
        self.task_create_data = {
            'name': 'test_name',
            'status': self.status.id,
            'creator': self.user.id,
            'executor': self.user.id
        }

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
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task creation was successful")
        )
