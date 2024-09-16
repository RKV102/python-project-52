from django import forms
from .models import User


class CreateUserForm(forms.ModelForm):
    short_name = forms.CharField(label='Имя')
    full_name = forms.CharField(label='Полное имя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    class Meta:
        model = User
        fields = ['short_name', 'full_name', 'password']
