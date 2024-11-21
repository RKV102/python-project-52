from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data)


class TestCreateLabels(TestCase):
    user_login_data = get_users_login_data()[0]
    label_create_data = get_fixture_data('labels.json')[0]

    def setUp(self):
        call_command('create_users')

    def test_create_label_by_unauthorized_user(self):
        response = self.client.post(
            reverse('labels_create'),
            data=self.label_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_create_label_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('labels_create'),
            data=self.label_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label creation was successful")
        )
