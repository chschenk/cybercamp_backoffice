from django import forms
from django_registration.forms import RegistrationForm
from cybercamp_backoffice.camp import models


class UserRegistrationForm(RegistrationForm):
    accept_privacy_policy = forms.BooleanField()
    class Meta(RegistrationForm.Meta):
        model = models.User
        fields = RegistrationForm.Meta.fields + ['first_name', 'last_name', 'address', 'zip_code', 'city', 'gender', 'birthday', ]