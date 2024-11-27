from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_user_login_data


class TestReadStatus(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = get_user_login_data()
        self.status = Status.objects.last()

    def test_read_status_by_unauthorized_user(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_read_status_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.get(reverse('statuses'))
        self.assertContains(response, self.status.name)
