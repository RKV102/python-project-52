from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_content


class TestReadLabel(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = get_content('user_login.json')
        self.label = Label.objects.last()

    def test_read_label_by_unauthorized_user(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_read_label_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.get(reverse('labels'))
        self.assertContains(response, self.label.name)
