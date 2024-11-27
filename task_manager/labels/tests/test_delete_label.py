from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.utils import get_message, create_users, get_user_login_data


class TestDeleteLabel(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json']

    def setUp(self):
        create_users()
        self.user = User.objects.last()
        self.user_login_data = get_user_login_data()
        self.label = Label.objects.last()
        self.status = Status.objects.last()
        self.task_create_data = {
            'id': 1,
            'name': 'test_name_1',
            'status': self.status.id,
            'creator': self.user.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        }

    def test_delete_label_by_unauthorized_user(self):
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("You are not logged in! Please log in")
        )

    def test_delete_label_by_authorized_user(self):
        self.client.login(**self.user_login_data)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label has been deleted")
        )
        response = self.client.get(reverse('labels'))
        self.assertNotContains(response, self.label.name)

    def test_delete_used_label(self):
        self.client.login(**self.user_login_data)
        self.client.post(
            reverse('tasks_create'),
            data=self.task_create_data
        )
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.pk}),
            follow=True
        )
        self.assertEqual(
            get_message(response),
            _("Label can't be deleted because it's used in the task")
        )
