from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n
from modeltranslation.forms import TranslationModelForm

from admin.models import Staff
from customer.models import Customer
from staring.models import *


class AdminLoginForm(forms.Form):
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


class ArticleForm(TranslationModelForm):
    class Meta:
        model = Article
        exclude = ["last_update", "create_date"]
        widgets = {
            "content": CKEditorWidget()
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ["uid", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ["user"]


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ["user"]


class CustomerSearch(forms.Form):
    tag = forms.ChoiceField(
        label=user_search_tag_text,
        choices=[('', '------')] + customer_tags,
        required=False,
    )

    vip = forms.ChoiceField(
        label=user_search_vip_text,
        choices=[('', '------')] + VipLevel,
        required=False
    )

    type = forms.ChoiceField(
        label=user_search_type_text,
        choices=[('', '------')] + user_Search_type,
        required=False,
    )

    detail = forms.CharField(
        label=user_search_detail_text,
        max_length=150,
        required=False,
    )

    def clean(self):
        if (self.cleaned_data.get("type") == "") ^ (self.cleaned_data.get("detail") == ""):
            raise ValidationError(message=user_search_errmsg_InsuffCond, code="InsufficientCondition")
        else:
            return self.cleaned_data


class StaffSearch(forms.Form):
    tag = forms.ChoiceField(
        label=user_search_tag_text,
        choices=[('', '------')] + staff_tags,
        required=False,
    )

    type = forms.ChoiceField(
        label=user_search_type_text,
        choices=[('', '------')] + user_Search_type,
        required=False,
    )

    detail = forms.CharField(
        label=user_search_detail_text,
        max_length=150,
        required=False,
    )

    def clean(self):
        if (self.cleaned_data.get("type") == "") ^ (self.cleaned_data.get("detail") == ""):
            raise ValidationError(message=user_search_errmsg_InsuffCond, code="InsufficientCondition")
        else:
            return self.cleaned_data


class NewsSectorForm(forms.ModelForm):
    class Meta:
        model = NewsSector
        exclude = ["id"]
