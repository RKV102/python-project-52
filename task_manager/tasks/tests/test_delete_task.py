from django.test import TestCase
from django.urls import reverse
from task_manager.tasks.models import Task
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data)


class TestDeleteTask(TestCase):
    user_login_data_1, user_login_data_2, *_ = get_users_login_data()
    tasks_data = get_fixture_data('tasks.json')

    def setUp(self):
        call_command('create_users')
        call_command('create_labels')
        call_command('create_statuses')
        call_command('create_tasks')
        self.created_task = Task.objects.last()

    def test_delete_task_by_unauthorized_user(self):
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.created_task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_task_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data_2,
        )
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.created_task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Task has been deleted")
        )
        response = self.client.get(reverse('tasks'))
        self.assertNotContains(response, self.created_task.name)

    def test_delete_task_by_another_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data_1,
        )
        response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.created_task.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Only the creator of the task can delete it")
        )
