from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from datetime import datetime, timedelta

from staring.models import User, Appointment
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
        self.fields["dob"].widget = forms.DateInput(format="%Y-%m-%d")
        self.fields["name"].required = True
        self.fields["email"].required = True


class MeetingSlotFilter(forms.Form):
    start_date = forms.DateField(
        label=_("开始日期"),
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "format": '%Y-%m-%d'}),
    )

    end_date = forms.DateField(
        label=_("截止日期"),
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "format": '%Y-%m-%d'}),
    )

    def clean_start_date(self):
        start = self.cleaned_data.get("start_date")
        if start < datetime.today().date():
            raise forms.ValidationError(_("Invalid Start date."))
        else:
            return start

    def clean_end_date(self):
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if end < datetime.today().date():
            raise forms.ValidationError(_("Invalid End date."))
        elif end - start > timedelta(days=14):
            raise forms.ValidationError(_("搜索间隔不得超过14天"))
        else:
            return end

    def clean(self):
        start = self.cleaned_data.get("start_date")
        end = self.cleaned_data.get("end_date")
        if end < start:
            raise forms.ValidationError(_("End date must be before start date."))


class AppointmentForm(forms.ModelForm):
    query = forms.CharField(
        label=appointment_consults_text,
        widget=forms.Textarea(
            attrs={"placeholder": appointment_consults_help_text}
        ),
    )

    class Meta:
        model = Appointment
        fields = ["title_prefix", "name", "email"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": appointment_name_placeholder_text}
            )
        }

