from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestDeleteTask(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        create_users()
        self.task = Task.objects.last()
        self.user_login_data = get_content('user_login.json')
        self.another_user_create_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'PsWd123*',
            'password2': 'PsWd123*'
        }

    def test_delete_task_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_task_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task has been deleted")
        )
        response = self.client.get(reverse('tasks'))
        self.assertNotContains(response, self.task.name)

    def test_delete_task_by_another_user(self):
        another_user_login_data = {
            'username': self.another_user_create_data['username'],
            'password': 'PsWd123*'
        }
        self.client.post(
            reverse('users_create'),
            data=self.another_user_create_data,
            follow=True
        )
        self.client.post(
            reverse('login'),
            data=another_user_login_data,
        )
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Only the creator of the task can delete it")
        )
