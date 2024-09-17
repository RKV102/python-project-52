from django import forms
from .models import User


class CreateUserForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    family = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = User
        fields = ['name', 'family', 'username', 'password']
