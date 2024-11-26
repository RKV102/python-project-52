from django.contrib.messages import get_messages
from task_manager.users.models import User


def get_message(response):
    messages = list(get_messages(response.wsgi_request))
    if messages:
        return messages[-1].message


def create_users():
    users = User.objects.all()
    for user in users:
        user.set_password(user.password)
        user.save()
