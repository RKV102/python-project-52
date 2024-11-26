from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users


class TestUpdateLabel(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = {
            'username': self.user.username,
            'password': 'PsWd123*'
        }
        self.label = Label.objects.last()
        self.label_update_data = {'name': 'test_label_new'}

    def test_update_label_by_unauthorized_user(self):
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}),
            data=self.label_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_update_label_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.pk}),
            data=self.label_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label has been updated")
        )
        response = self.client.get(reverse('labels'))
        self.assertContains(response, self.label_update_data['name'])
