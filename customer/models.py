from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from django_countries.fields import CountryField

from staring.customerSettings import *
from staring.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )

    contact_type = models.CharField(
        verbose_name=_("联系方式"),
        max_length=20,
        choices=ContactTypes,
        default=ContactTypes[0][0]
    )

    contact_detail = models.CharField(
        verbose_name=_("联系号码"),
        max_length=150,
        blank=True,
        null=True
    )

    nationality = CountryField(
        verbose_name=_("国籍")
    )

    intention = models.CharField(
        verbose_name=_("意向项目"),
        choices=Intentions,
        max_length=4
    )

    vip_lv = models.IntegerField(
        verbose_name=_("用户等级"),
        choices=VipLevel,
        default=1
    )

