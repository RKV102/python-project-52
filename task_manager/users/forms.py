from django.contrib.auth.forms import (UserCreationForm
                                       as DjangoUserCreationForm,
                                       UserChangeForm
                                       as DjangoUserChangeForm,
                                       SetPasswordMixin)
from ..mixins.forms import UserMixin


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
