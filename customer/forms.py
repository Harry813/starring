from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.models import User
from .models import Consult
from staring.text import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ["name", "email", "contact_detail", "query"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": consult_name_placeholder})
        self.fields["email"].widget.attrs.update({"placeholder": consult_email_placeholder})
        self.fields["contact_detail"].widget.attrs.update({"placeholder": consult_contact_placeholder})
        self.fields["query"].widget.attrs.update({"placeholder": consult_query_placeholder})


class CustomerLoginForm(forms.Form):
    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label=user_username_text,
        max_length=150,
        min_length=8,
        validators=[username_validator],
        help_text=user_username_help_text,
        error_messages={
            "invalid": user_username_err_invalid,
            "max_length": user_username_err_max,
            "min_length": user_username_err_min,
            "UserNotExist": UserNotExist_text,
        },
    )

    password = forms.CharField(
        label=user_password_text,
        max_length=128,
        min_length=8,
        widget=forms.PasswordInput,
        help_text=user_password_help_text,
        error_messages={
            "invalid": user_password_err_invalid,
            "max_length": user_password_err_max_length,
            "min_length": user_password_err_min_length
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username):
            return username
        else:
            raise ValidationError(UserNotExist_text, code="UserNotExist")


class CustomerRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=user_password_text,
        max_length=128,
        widget=forms.PasswordInput,
        help_text=user_password_help_text
    )

    password2 = forms.CharField(
        label=user_confirm_text,
        max_length=128,
        widget=forms.PasswordInput
    )

    def clean_password1(self):
        paswd1 = self.cleaned_data.get("password1")
        if validate_password(paswd1) is None:
            return paswd1

    def clean_password2(self):
        paswd1 = self.cleaned_data.get('password1')
        paswd2 = self.cleaned_data.get('password2')
        if paswd1 == paswd2:
            return paswd2
        else:
            raise forms.ValidationError(paswd_errmsg_NOT_match, code="paswdNotMatch")

    class Meta:
        model = User
        fields = ["name", "email", "countryCode", "tele", "username", "dob"]

    def __init__(self, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)
        self.fields["dob"].help_text = "YYYY/MM/DD"
        self.fields["name"].required = True
        self.fields["email"].required = True

