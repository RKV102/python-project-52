from django.test import TestCase
from .models import Status
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class StatusTestCase(TestCase):

    def setUp(self):
        user_create_data = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'password1': 'PsWd123*',
            'password2': 'PsWd123*'
        }
        user_login_data = {
            'username': 'test_username',
            'password': 'PsWd123*'
        }
        self.status_create_data = {
            'name': 'test_status_name'
        }
        self.status_update_data = {
            'name': 'test_status_name_new'
        }
        self.client.post(
            reverse('users_create'),
            data=user_create_data,
        )
        self.client.post(
            reverse('login'),
            data=user_login_data
        )

    def get_message(self, response):
        messages = list(get_messages(response.wsgi_request))
        if messages:
            return messages[-1].message

    def test_create_status(self):
        statuses_count = Status.objects.count()
        response = self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data,
            follow=True
        )
        self.assertEqual(Status.objects.count(), statuses_count + 1)
        self.assertEqual(
            self.get_message(response),
            _("Status creation was successful")
        )

    def test_read_status(self):
        self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data
        )
        response = self.client.get(reverse('statuses'))
        self.assertContains(
            response,
            self.status_create_data['name'],
        )

    def test_update_status(self):
        self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data
        )
        created_status = Status.objects.last()
        response = self.client.post(
            reverse(
                'statuses_update',
                kwargs={'pk': created_status.pk}
            ),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            self.get_message(response),
            _("Status has been updated")
        )
        response = self.client.get(reverse('statuses'))
        self.assertContains(
            response,
            self.status_update_data['name'],
        )

    def test_delete_status(self):
        self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data
        )
        created_status = Status.objects.last()
        response = self.client.post(
            reverse(
                'statuses_delete',
                kwargs={'pk': created_status.pk}
            ),
            data=self.status_update_data,
            follow=True
        )
        self.assertEqual(
            self.get_message(response),
            _("Status has been deleted")
        )
        response = self.client.get(reverse('statuses'))
        self.assertNotContains(
            response,
            self.status_create_data['name'],
        )
