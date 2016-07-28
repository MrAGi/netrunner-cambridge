from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation  import ugettext_lazy as _

from registration.users import UserModel, UsernameField
from registration.forms import RegistrationFormUniqueEmail

User = UserModel()

class RegistrationFormFullName(RegistrationFormUniqueEmail):
    """
    Subclass of `RegistrationFormUniqueEmail` which adds first and last
    names
    """

    first_name = forms.CharField(label=_("First name"),
                                max_length=60,
                                min_length=2)
    last_name = forms.CharField(label=_("Last name"),
                                max_length=120,
                                min_length=2)

    class Meta:
        model = User
        fields = (UsernameField(), "first_name", UsernameField(), "last_name", UsernameField(), "email")