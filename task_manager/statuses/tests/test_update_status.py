from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, get_users_login_data, create_users


class TestUpdateStatus(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_users_login_data()[0]
        self.status_update_data = {
            'name': 'test_status_new',
        }
        self.created_status = Status.objects.last()

    def test_update_status_by_unauthorized_user(self):
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.created_status.pk}),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_status_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.created_status.pk}),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status has been updated")
        )
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, self.status_update_data['name'])
