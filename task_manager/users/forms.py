from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import (UserCreationForm
                                       as DjangoUserCreationForm,
                                       UserChangeForm
                                       as DjangoUserChangeForm,
                                       SetPasswordMixin,
                                       UsernameField)


class UserMixin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        field_classes = {"username": UsernameField}


class UserCreationForm(UserMixin, DjangoUserCreationForm):
    pass


class UserChangeForm(UserMixin, SetPasswordMixin, DjangoUserChangeForm):
    password1, password2 = SetPasswordMixin.create_password_fields()
    password = None

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def _post_clean(self):
        super()._post_clean()
        self.validate_password_for_user(self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        if commit and hasattr(self, "save_m2m"):
            self.save_m2m()
        return user
