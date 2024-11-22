from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data, create_users)


class TestCreateStatus(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        create_users()
        self.user_login_data = get_users_login_data()[0]
        self.status_create_data = get_fixture_data('statuses.json')[0]

    def test_create_status_by_unauthorized_user(self):
        response = self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_create_status_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('statuses_create'),
            data=self.status_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Status creation was successful")
        )