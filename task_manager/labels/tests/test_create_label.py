from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestCreateLabels(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = get_content('user_login.json')
        self.label_create_data = {'name': 'test_label_name'}

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
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('labels_create'),
            data=self.label_create_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label creation was successful")
        )
