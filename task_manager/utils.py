from django.contrib.messages import get_messages
from task_manager.users.models import User
from task_manager.settings import BASE_DIR
import json


def get_message(response):
    messages = list(get_messages(response.wsgi_request))
    if messages:
        return messages[-1].message


def create_users():
    users = User.objects.all()
    for user in users:
        user.set_password(user.password)
        user.save()


def get_user_login_data():
    login_data_path = str(BASE_DIR / 'task_manager' / 'fixtures'
                          / 'user_login.json')
    with open(login_data_path) as content:
        login_data = json.load(content)
        return login_data
