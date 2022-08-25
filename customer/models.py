from django.core.validators import MinLengthValidator
from django.db import models
from django.shortcuts import get_list_or_404
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from django_countries.fields import CountryField

from staring.customerSettings import *
from staring.models import User, CRS
from staring.text import *


class Customer(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )

    contact_type = models.CharField(
        verbose_name=customer_contact_type_text,
        max_length=20,
        choices=ContactTypes,
        blank=True
    )

    contact_detail = models.CharField(
        verbose_name=customer_contact_detail_text,
        max_length=150,
        blank=True,
        null=True
    )

    nationality = CountryField(
        verbose_name=customer_nationality_text,
        blank=True
    )

    intention = models.CharField(
        verbose_name=customer_intention_text,
        choices=Intentions,
        max_length=4,
        blank=True
    )

    extra = models.TextField(
        verbose_name=customer_extra_text,
        blank=True
    )

    vip_lv = models.IntegerField(
        verbose_name=customer_vip_lv_text,
        choices=VipLevel,
        default=0
    )

    tag = models.CharField(
        verbose_name=customer_tag_text,
        max_length=10,
        blank=True,
        choices=customer_tags
    )

    @property
    def evaluations(self):
        return list(CRS.objects.filter(customer=self))

    def clean_extra(self):
        if self.intention == "OTHR":
            self.extra.required = True

    def __str__(self):
        return self.user.get_display_name()


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
