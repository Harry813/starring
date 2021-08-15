import uuid

from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from staring.customerSettings import *

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=_("电话格式错误，请使用格式 +NNxxxxxxxxxx"))


class User(AbstractUser):
    # UID 用户ID，全局唯一
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # username 用户名，全局唯一
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('用户名'),
        max_length=150,
        min_length=8,
        unique=True,
        help_text=_('必填，至多150字符（仅可包含大小写字母、数字以及@/./+/-/_）'),
        validators=[username_validator],
        error_messages={
            'unique': _("用户名已存在"),
            'invalid': _("无效的用户名"),
            'max_length': _("用户名长度不得超过150字符"),
            'min_length': _("用户名长度不得超过150字符"),
        },
    )

    first_name = None
    last_name = None
    name = models.CharField(_('真实姓名'), max_length=150, blank=True)

    email = models.EmailField(_('邮箱地址'), blank=True)
    tele = models.CharField

    nationality = CountryField(
        _("国籍"),
        required=True
    )

    intention = models.CharField(
        _("意向项目"),
        choices=Intentions,
        max_length=4
    )

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
