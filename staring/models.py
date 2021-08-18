import datetime
import uuid

from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from staring.customerSettings import *
from staring.phoneCode import *

phone_regex = RegexValidator(regex=r'[0-9]{0,14}$',
                             message=_("电话格式错误"),
                             code="InvalidPhone")


class User(AbstractUser):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('用户名'),
        max_length=150,
        unique=True,
        help_text=_('必填，至多150字符（仅可包含大小写字母、数字以及@/./+/-/_）'),
        validators=[username_validator, MinLengthValidator(8)],
        error_messages={
            'unique': _("用户名已存在"),
            'invalid': _("无效的用户名"),
            'max_length': _("用户名长度不得超过150字符"),
            'min_length': _("用户名长度不得少于8字符"),
        },
    )

    first_name = None
    last_name = None
    name = models.CharField(_('真实姓名'), max_length=150, blank=True)
    dob = models.DateField(
        _('生日'),
        validators=[MinValueValidator(datetime.date(1900, 1, 1)),
                    MaxValueValidator(datetime.date.today())]
    )

    def get_age(self):
        age = datetime.date.today().year - self.dob.year
        return age

    email = models.EmailField(_('邮箱地址'), blank=True)

    countryCode = models.CharField(
        _("冠码"),
        max_length=10,
        choices=phone_codes,  # sorted by country name
        # choices=sorted_phone_codes,  # sorted by country code
        default='1'
    )
    tele = models.CharField(
        _("电话号码"),
        validators=[phone_regex]
    )

    def get_phone(self):
        phone = "+{}-{}".format(self.countryCode, self.tele)
        return phone

    contact_type = models.CharField(
        _("联系方式"),
        max_length=20,
        choices=ContactTypes,
        default=ContactTypes[0][0]
    )

    contact_detail = models.CharField(
        _("联系号码"),
        max_length=150,
        blank=True,
        null=True
    )

    nationality = CountryField(
        _("国籍"),
        required=True
    )

    intention = models.CharField(
        _("意向项目"),
        choices=Intentions,
        max_length=4
    )

    vip_lv = models.IntegerField(
        _("用户等级"),
        choices=VipLevel,
        default=1
    )

    # hidden, can only accessed by admins
    is_staff = models.BooleanField(
        _('员工权限'),
        default=False,
        help_text=_('指定用户是否可以登录到此管理站点'),
    )
    is_active = models.BooleanField(
        _('活跃状态'),
        default=True,
        help_text=_(
            '指定是否应将此用户视为活动用户，'
            '请取消选择此项代替删除帐户。'
        ),
    )
    date_joined = models.DateTimeField(_('注册日期'), default=timezone.now)
    last_change = models.DateTimeField(
        _("最后修改"),
        auto_now=True
    )
