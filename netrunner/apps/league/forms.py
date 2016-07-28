from registration.forms import RegistrationFormUniqueEmail
from django import forms

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