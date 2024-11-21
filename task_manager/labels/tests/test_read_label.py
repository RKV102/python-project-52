from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_users_login_data,
                                get_fixture_data)


class TestReadLabel(TestCase):
    user_login_data = get_users_login_data()[0]
    label_data = get_fixture_data('labels.json')[0]

    def setUp(self):
        call_command('create_users')
        call_command('create_labels')

    def test_read_label_by_unauthorized_user(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_read_label_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.get(reverse('labels'))
        self.assertContains(response, self.label_data['name'])
