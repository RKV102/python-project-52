from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from task_manager.utils import (get_message, get_fixture_data,
                                get_users_login_data)


class TestDeleteLabel(TestCase):
    user_login_data = get_users_login_data()[0]
    label_data = get_fixture_data('labels.json')[0]

    def setUp(self):
        call_command('create_users')
        call_command('create_labels')
        self.created_label = Label.objects.last()

    def test_delete_label_by_unauthorized_user(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.created_label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_label_by_authorized_user(self):
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.created_label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label has been deleted")
        )
        response = self.client.get(reverse('labels'))
        self.assertNotContains(response, self.created_label.name)

    def test_delete_used_label(self):
        call_command('create_statuses')
        call_command('create_tasks')
        self.client.post(
            reverse('login'),
            data=self.user_login_data,
        )
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.created_label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label can't be deleted because it's used in the task")
        )
