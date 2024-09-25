from django.contrib.auth.models import User
from django.contrib.auth.forms import (UserCreationForm
                                       as DjangoUserCreationForm,
                                       UserChangeForm
                                       as DjangoUserChangeForm,
                                       SetPasswordMixin)


class UserCreationForm(DjangoUserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserChangeForm(SetPasswordMixin, DjangoUserChangeForm):
    password1, password2 = SetPasswordMixin.create_password_fields()
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean(self):
        self.validate_passwords()
        return super().clean()

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        self.validate_password_for_user(self.instance)

    def save(self, commit=True):
        user = super().save(commit=False)
        user = self.set_password_and_save(user, commit=commit)
        if commit and hasattr(self, "save_m2m"):
            self.save_m2m()
        return user
