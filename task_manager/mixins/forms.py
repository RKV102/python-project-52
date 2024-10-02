from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UsernameField


class UserMixin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        field_classes = {"username": UsernameField}
