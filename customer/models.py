from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from django_countries.fields import CountryField

from staring.customerSettings import *
from staring.models import User
from staring.text import *


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


class Consult(models.Model):
    name = models.CharField(
        verbose_name=consult_name_text,
        max_length=150,
        validators=[MinLengthValidator(2)],
        error_messages={
            "required": consult_name_err_required,
            "min_length": consult_name_err_min_length,
            "max_length": consult_name_err_max_length,
        }
    )

    email = models.EmailField(
        verbose_name=consult_email_text,
        error_messages={
            "required": consult_email_err_required,
            "invalid": consult_email_err_invalid,
            "max_length": consult_email_err_max_length
        }
    )

    contact_detail = models.CharField(
        verbose_name=consult_contact_text,
        max_length=150,
        error_messages={
            "required": consult_contact_err_required,
            "max_length": consult_contact_err_max_length,
        }
    )

    query = models.TextField(
        verbose_name=consult_query_text,
        error_messages={
            "required": consult_query_err_required
        }
    )

    status = models.BooleanField(
        verbose_name=consult_status_text,
        default=True
    )

    create_date = models.DateTimeField(
        verbose_name=consult_create_date_text,
        auto_now_add=True
    )

    @property
    def is_open(self):
        return self.status is True

    @property
    def is_close(self):
        return self.status is False
