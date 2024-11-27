from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestDeleteStatus(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_content('user_login.json')
        self.status = Status.objects.last()
        self.task_create_data = get_content('task_create.json')

    def test_delete_status_by_unauthorized_user(self):
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_status_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status has been deleted")
        )
        response = self.client.get(reverse('statuses'))
        self.assertNotContains(response, self.status.name)

    def test_delete_used_status(self):
        self.client.login(**self.user_login_data)
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data
        )
        response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status can't be deleted because it's used in the task")
        )
