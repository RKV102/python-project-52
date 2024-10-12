from django.test import TestCase
from .models import Label


class LabelTestCase(TestCase):

    def setUp(self):
        Label.objects.create(name='label_task')

    def test_label_can_be_created(self):
        assert Label.objects.last().name == 'label_task'

    def test_label_can_be_updated(self):
        task = Label.objects.last()
        task.name = 'test_name'
        task.save()
        assert Label.objects.last().name == 'test_name'

    def test_label_can_be_deleted(self):
        Label.objects.last().delete()
        assert not Label.objects.all()
