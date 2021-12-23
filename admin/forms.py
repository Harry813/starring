from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import ASCIIUsernameValidator
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
        # widgets = {
        #     'content': CKEditorUploadingWidget(),
        # }


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


class StaffCreateForm(forms.Form):
    username = forms.CharField(
        label=user_username_text,
        max_length=150,
        min_length=8,
        help_text=user_username_help_text,
        validators=[ASCIIUsernameValidator],
        error_messages={
            "required": user_username_err_require,
            "max_length": user_username_err_max,
            "min_length": user_username_err_min,
            "invalid": user_username_err_invalid
        }
    )

    password1 = forms.CharField(
        label=user_password_text,
        min_length=8,
        max_length=128,
        help_text=user_password_help_text,
        widget=forms.PasswordInput(),
        error_messages={
            "required": user_password_err_empty,
            "min_length": user_password_err_min_length,
            "max_length": user_password_err_max_length,
        }
    )

    password2 = forms.CharField(
        label=user_confirm_text,
        min_length=8,
        max_length=128,
        help_text=user_confirm_help_text,
        widget=forms.PasswordInput(),
        error_messages={
            "required": user_confirm_err_require,
            "min_length": user_confirm_err_min_length,
            "max_length": user_confirm_err_max_length,
        }
    )

    name = forms.CharField(
        label=user_name_text,
    )

    email = forms.EmailField(
        label=user_email_text,
    )

    code = forms.ChoiceField(
        label=user_countryCode_text,
        choices=sorted_phone_codes
    )

    tele = forms.CharField(
        label=user_tele_text,
        validators=[phone_regex]
    )

    dob = forms.DateField(
        label=user_dob_text,
        required=False,
        input_formats=['%Y/%m/%d', '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        help_text="YYYY/MM/DD"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username):
            raise ValidationError(
                _('用户名已存在'),
                code="unique"
            )
        else:
            return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if validate_password(password1) is None:
            return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 == password2:
            return password2
        else:
            raise forms.ValidationError(paswd_errmsg_NOT_match, code="paswdNotMatch")

    def save(self):
        pass


class CustomerSearch(forms.Form):
    tag = forms.ChoiceField(
        label=user_search_tag_text,
        choices=[('', '--------')] + customer_tags,
        required=False,
    )

    vip = forms.ChoiceField(
        label=user_search_vip_text,
        choices=[('', '--------')] + VipLevel,
        required=False
    )

    type = forms.ChoiceField(
        label=user_search_type_text,
        choices=[('', '--------')] + user_Search_type,
        required=False,
    )

    detail = forms.CharField(
        label=user_search_detail_text,
        required=False,
    )

    def clean(self):
        if (self.cleaned_data.get("type") == "") ^ (self.cleaned_data.get("detail") == ""):
            raise ValidationError(message=search_errmsg_InsuffCond, code="InsufficientCondition")
        else:
            return self.cleaned_data


class StaffSearch(forms.Form):
    tag = forms.ChoiceField(
        label=user_search_tag_text,
        choices=[('', '--------')] + staff_tags,
        required=False,
    )

    type = forms.ChoiceField(
        label=user_search_type_text,
        choices=[('', '--------')] + article_Search_type,
        required=False,
    )

    detail = forms.CharField(
        label=user_search_detail_text,
        max_length=150,
        required=False,
    )

    def clean(self):
        if (self.cleaned_data.get("type") == "") ^ (self.cleaned_data.get("detail") == ""):
            raise ValidationError(message=search_errmsg_InsuffCond, code="InsufficientCondition")
        else:
            return self.cleaned_data


class NewsSectorForm(forms.ModelForm):
    class Meta:
        model = NewsSector
        exclude = ["id"]


class NewsSearchForm(forms.Form):
    sector = forms.ModelChoiceField(
        queryset=None,
        label=newsSearch_sector_text,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'].queryset = NewsSector.objects.all()


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"


class ArticleSearchForm(forms.Form):
    status = forms.ChoiceField(
        label=article_status_text,
        choices=[('', '--------')] + ArticleStatus,
        required=False
    )

    lv_require = forms.ChoiceField(
        label=article_lv_require_text,
        choices=[(-1, '--------')] + VipLevel,
        required=False
    )

    search_type = forms.ChoiceField(
        label=articleSearch_type_text,
        choices=[('', '--------')] + article_Search_type,
        required=False
    )

    detail = forms.CharField(
        label=articleSearch_detail_text,
        required=False,
    )

    def clean(self):
        if (self.cleaned_data.get("type") == "") ^ (self.cleaned_data.get("detail") == ""):
            raise ValidationError(message=search_errmsg_InsuffCond, code="InsufficientCondition")
        else:
            return self.cleaned_data


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = MeetingSlot
        fields = ["date", "time", "availability"]


class NaviSectorForm(TranslationModelForm):
    def save(self, commit=True):
        sec = super(NaviSectorForm, self).save(commit=False)

        # Update all the sector orders
        sector_list = NavigatorSector.objects.all()
        for s in range(len(sector_list)):
            sector_list[s].order = s
        sec.order = len(sector_list)
        if commit:
            sec.save()
        return sec

    class Meta:
        model = NavigatorSector
        fields = ["name"]
