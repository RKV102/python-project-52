from django import forms
from .models import User


HELP_TEXTS = {
    'username': 'Обязательное поле. Не более 15 символов.',
    'password': 'Обязательное поле. Не более 20 символов.'
}


class UserForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    family = forms.CharField(label='Фамилия')
    username = forms.CharField(
        label='Имя пользователя',
        help_text=HELP_TEXTS['username']
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль',
        help_text=HELP_TEXTS['password']
    )

    class Meta:
        model = User
        fields = ['name', 'family', 'username', 'password']
