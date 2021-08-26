import datetime
import uuid

from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from ckeditor.fields import RichTextField

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
        verbose_name=_('用户名'),
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
    name = models.CharField(
        verbose_name=_('真实姓名'),
        max_length=150,
        blank=True
    )
    dob = models.DateField(
        verbose_name=_('生日'),
        validators=[MinValueValidator(datetime.date(1900, 1, 1)),
                    MaxValueValidator(datetime.date.today())]
    )

    def get_age(self):
        age = datetime.date.today().year - self.dob.year
        return age

    email = models.EmailField(_('邮箱地址'), blank=True)

    countryCode = models.CharField(
        verbose_name=_("冠码"),
        max_length=10,
        choices=phone_codes,  # sorted by country name
        # choices=sorted_phone_codes,  # sorted by country code
        default='1'
    )
    tele = models.CharField(
        verbose_name=_("电话号码"),
        max_length=15,
        validators=[phone_regex]
    )

    def get_phone(self):
        phone = "+{}-{}".format(self.countryCode, self.tele)
        return phone

    # hidden, can only accessed by admins
    is_staff = None
    is_active = models.BooleanField(
        verbose_name=_('活跃状态'),
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


class Article(models.Model):
    # todo: 添加cover
    author = models.CharField(
        verbose_name=_("作者"),
        max_length=150,
    )

    status = models.CharField(
        verbose_name=_("文章状态"),
        max_length=10
    )

    lv_require = models.IntegerField(
        verbose_name=_("需求用户等级"),
        choices=VipLevel,
        default=1
    )

    description = models.CharField(
        verbose_name=_("META标签-描述"),
        max_length=300,
        help_text=_(
            "本标签将不在页面中显示。上限300字符"
        )
    )

    keywords = models.CharField(
        verbose_name=_("META标签-关键词"),
        max_length=150,
        help_text=_(
            "本标签将不在页面中显示，关键字之间请使用逗号分割。上限150字符"
        )
    )

    content = RichTextField(
        verbose_name=_("文章主体")
    )

    create_date = models.DateTimeField(
        verbose_name=_("创建时间"),
        default=timezone.now
    )

    last_update = models.DateTimeField(
        verbose_name=_("最后修改"),
        auto_now=True
    )
