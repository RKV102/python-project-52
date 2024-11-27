from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestUpdateStatus(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = get_content('user_login.json')
        self.status = Status.objects.last()
        self.status_update_data = {'name': 'test_status_new'}

    def test_update_status_by_unauthorized_user(self):
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_status_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status.pk}),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status has been updated")
        )
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, self.status_update_data['name'])
