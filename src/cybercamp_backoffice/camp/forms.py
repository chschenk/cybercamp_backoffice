from django import forms
from django_registration.forms import RegistrationForm
from cybercamp_backoffice.camp.models import User


class UserRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User