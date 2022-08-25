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

from datetime import datetime, date, time, timedelta
from dateutil import rrule
from .utils import TIMESLOT_INTERVAL, default_timeslot_offset_options, time_delta_total_seconds, TIMESLOT_DURATION

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
        exclude = ["last_update", "create_date", "view_count"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ["uid", "password"]


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
        label=email_text,
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
    class Meta:
        model = NavigatorSector
        fields = ["name", "order"]
        widgets = {'order': forms.HiddenInput()}


class NavigatorItemForm(TranslationModelForm):
    reorder = forms.IntegerField(
        initial=0,
        required=False,
        label=navi_item_order_text
    )

    def clean_reorder(self):
        reorder = self.cleaned_data.get("reorder")
        if reorder is None or reorder <= 0:
            return -1
        else:
            return reorder - 1

    def clean_url(self):
        t = self.cleaned_data.get("type")
        url = self.cleaned_data.get("url")
        if t == "URL" and url == "":
            raise ValidationError(navi_item_url_err_empty)
        else:
            return url

    def clean_article(self):
        t = self.cleaned_data.get("type")
        article = self.cleaned_data.get("article")
        if t == "ARTICLE" and article == "":
            raise ValidationError(navi_item_article_err_empty)
        else:
            # a = Article.objects.get(id=article)
            return article

    def __init__(self, *args, **kwargs):
        super(NavigatorItemForm, self).__init__(*args, **kwargs)
        self.fields["article"].required = False
        self.fields["url"].initial = "#"

    class Meta:
        model = NavigatorItem
        exclude = ["order"]


class IndexListSectorForm(TranslationModelForm):
    class Meta:
        model = IndexListSector
        fields = "__all__"


class IndexListItemForm(TranslationModelForm):
    reorder = forms.IntegerField(
        label=index_list_item_order_text,
        min_value=1,
        required=False
    )

    def clean_reorder(self):
        reorder = self.cleaned_data.get("reorder")
        if reorder is None or reorder <= 0:
            return -1
        else:
            return reorder - 1

    def clean_url(self):
        t = self.cleaned_data.get("type")
        url = self.cleaned_data.get("url")
        if t == "URL" and url == "":
            raise ValidationError(navi_item_url_err_empty)
        else:
            return url

    def clean_article(self):
        t = self.cleaned_data.get("type")
        article = self.cleaned_data.get("article")
        if t == "ARTICLE" and article == "":
            raise ValidationError(navi_item_article_err_empty)
        else:
            # a = Article.objects.get(id=article)
            return article

    def __init__(self, *args, **kwargs):
        super(IndexListItemForm, self).__init__(*args, **kwargs)
        self.fields["article"].required = False
        self.fields["url"].initial = "#"

    class Meta:
        model = IndexListItem
        exclude = ["order"]


class SlotGeneratorForm(forms.Form):
    start_date = forms.DateField(
        label=start_date_text,
    )

    end_date = forms.DateField(
        label=end_date_text,
    )

    start_time = forms.TimeField(
        label=slot_start_time_text,
    )

    end_time = forms.TimeField(
        label=slot_end_time_text,
    )

    weekends = forms.BooleanField(
        label=slot_weekends_text,
        initial=False,
        required=False,
    )

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]
        if start_date < date.today():
            raise ValidationError(_("Invalid Date"))
        else:
            return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data["end_date"]
        start_date = self.cleaned_data["start_date"]
        if end_date < start_date:
            raise ValidationError(_("Invalid Date"))
        else:
            return end_date

    def clean_end_time_delta(self):
        end_time_delta = self.cleaned_data["end_time"]
        start_time_delta = self.cleaned_data["start_time"]
        if end_time_delta < start_time_delta:
            raise ValidationError(_("Invalid Time"))

    def save(self):
        start_date = self.cleaned_data.get("start_date")
        start_time = self.cleaned_data.get("start_time")
        end_date = self.cleaned_data.get("end_date")
        end_time = self.cleaned_data.get("end_time")
        weekends = self.cleaned_data.get("weekends")

        day_range = [date.fromordinal(i) for i in range(start_date.toordinal(), end_date.toordinal())]

        if not weekends:
            day_range = [d for d in day_range if d.weekday() <= 4]
            for d in day_range:
                start_datetime = datetime.combine(d, start_time)
                end_datetime = datetime.combine(d, end_time)
                MeetingSlot.objects.create(start_datetime=start_datetime, end_datetime=end_datetime)


class SlotEditForm(forms.Form):
    date = forms.DateField(
        label=_("日期"),
    )

    start_time = forms.TimeField(
        label=_("开始时间"),
    )

    end_time = forms.TimeField(
        label=_("结束时间"),
    )

    # availability = forms.IntegerField(
    #     label=_("剩余"),
    #     min_value=0,
    # )

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if start_time > end_time:
            raise forms.ValidationError(_("Illegal Start Time"))
        else:
            return start_time

    def clean_end_date(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if end_time < start_time:
            raise forms.ValidationError(_("Illegal End Time"))
        else:
            return end_time


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["status"]


class AppointmentAllocateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["staff"]


class IndexSidebarForm(forms.ModelForm):
    reorder = forms.IntegerField(
        label=index_list_item_order_text,
        min_value=1,
        required=False
    )

    class Meta:
        model = IndexSidebarItem
        exclude = ["order"]

    def __init__(self, *args, **kwargs):
        super(IndexSidebarForm, self).__init__(*args, **kwargs)
        self.fields["url"].initial = "#"


class AppointmentFilterForm(forms.Form):
    start_datetime = forms.DateTimeField(
        label=_("起始时间"),
        required=False,
    )

    end_datetime = forms.DateTimeField(
        label=_("结束时间"),
        required=False,
    )

    status = forms.MultipleChoiceField(
        label=_("状态"),
        choices=meeting_status,
        required=False,
        help_text=_("按住ctrl键可多选"),
    )

    keyword = forms.CharField(
        label=_("关键字"),
        required=False,
        help_text=_("可搜索ID/预留名称/E-mail"),
    )


class MeetingUpdateForm(forms.ModelForm):
    class Meta:
        model = MeetingUpdate
        fields = ["title", "attachment", "message", "appointment"]


class OrderSearchForm(forms.Form):
    start_date = forms.DateField(
        label=_("起始日期"),
        required=False,
    )

    end_date = forms.DateField(
        label=_("结束日期"),
        required=False,
    )

    status = forms.MultipleChoiceField(
        label=_("状态"),
        choices=[
            ("CREATED", _("已创建")),
            ("COMPLETED", _("已通过")),
            ("PENDING", _("待处理")),
            ("CANCELED", _("已取消")),
            ("REFUNDED", _("已退款")),
        ],
        required=False,
        help_text=_("按住ctrl键可多选"),
    )

    type = forms.ChoiceField(
        label=_("类型"),
        choices=[
            ('', '--------'),
            ("ID", _("ID")),
            ("KEYWORD", _("关键字")),
        ],
        required=False,
    )

    detail = forms.CharField(
        required=False,
    )

    def clean(self):
        cleaned_data = super(OrderSearchForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("Invalid Date"))

        detail = cleaned_data.get("detail")
        search_type = cleaned_data.get("type")
        if detail and not search_type:
            raise forms.ValidationError(_("Invalid Search Type"))
        return cleaned_data
