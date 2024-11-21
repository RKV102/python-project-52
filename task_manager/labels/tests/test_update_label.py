from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, get_users_login_data


class TestUpdateLabel(TestCase):
    user_login_data = get_users_login_data()[0]
    label_update_data = {
        'name': 'test_label_new',
    }

    def setUp(self):
        call_command('create_users')
        call_command('create_labels')
        self.created_label = Label.objects.last()

    def test_update_label_by_unauthorized_user(self):
        response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.created_label.pk}),
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
            reverse('labels_update', kwargs={'pk': self.created_label.pk}),
            data=self.label_update_data,
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label has been updated")
        )
        response = self.client.get(reverse('labels'))
        self.assertContains(response, self.label_update_data['name'])
