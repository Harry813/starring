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
from staring.text import *

phone_regex = RegexValidator(regex=r'[0-9]{0,14}$',
                             message=user_tele_err_invalid,
                             code="InvalidPhone")


class User(AbstractUser):
    uid = models.UUIDField(
        verbose_name=user_uid_text,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    def get_uid_as_string(self):
        return str(self.uid).replace('-', '')

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name=user_username_text,
        max_length=150,
        unique=True,
        help_text=user_username_help_text,
        validators=[username_validator, MinLengthValidator(8)],
        error_messages={
            'unique': user_username_err_unique,
            'invalid': user_username_err_invalid,
            'max_length': user_username_err_max,
            'min_length': user_username_err_min,
        },
    )

    password = models.CharField(
        verbose_name=_('password'),
        max_length=128,
        help_text=user_password_help_text,
        error_messages={
            "invalid": user_password_err_invalid,
            "max_length": user_password_err_max_length,
            "min_length": user_password_err_min_length
        }
    )

    first_name = None
    last_name = None
    name = models.CharField(
        verbose_name=user_name_text,
        max_length=150,
        blank=True
    )

    def get_display_name(self):
        if self.name:
            return self.name
        elif self.username:
            return self.username

    dob = models.DateField(
        verbose_name=user_dob_text,
        validators=[
            MinValueValidator(datetime.date(1900, 1, 1)),
            MaxValueValidator(datetime.date.today())
        ],
        default=datetime.date(1900, 1, 1)
    )

    def get_age(self):
        age = datetime.date.today().year - self.dob.year
        return age

    email = models.EmailField(
        verbose_name=user_email_text,
        blank=True
    )

    countryCode = models.CharField(
        verbose_name=user_countryCode_text,
        max_length=10,
        choices=phone_codes,  # sorted by country name
        # choices=sorted_phone_codes,  # sorted by country code
        default='1'
    )

    tele = models.CharField(
        verbose_name=user_tele_text,
        max_length=15,
        validators=[phone_regex]
    )

    avatar = models.ImageField(
        verbose_name=user_avatar_text,
        default="",
        upload_to="avatar",
        blank=True
    )

    def get_phone(self):
        phone = "+{}-{}".format(self.countryCode, self.tele)
        return phone

    # hidden, can only accessed by admins
    is_active = models.BooleanField(
        verbose_name=user_active_text,
        default=True,
        help_text=user_active_help_text,
    )
    date_joined = models.DateTimeField(
        verbose_name=user_date_join_text,
        default=timezone.now
    )

    last_change = models.DateTimeField(
        verbose_name=user_last_change_text,
        auto_now=True
    )

    def __str__(self):
        return self.get_display_name()


class Article(models.Model):
    status = models.CharField(
        verbose_name=article_status_text,
        max_length=10,
        choices=ArticleStatus,
    )

    title = models.CharField(
        verbose_name=article_title_text,
        max_length=150,
    )

    author = models.CharField(
        verbose_name=article_author_text,
        max_length=150,
    )

    lv_require = models.IntegerField(
        verbose_name=article_lv_require_text,
        choices=VipLevel,
        default=0
    )

    copyable = models.BooleanField(
        verbose_name=article_copyable_text,
        default=False,
        help_text=article_copyable_help_text
    )

    description = models.CharField(
        verbose_name=article_meta_description_text,
        max_length=300,
        help_text=article_meta_description_help_text,
        blank=True
    )

    keywords = models.CharField(
        verbose_name=article_meta_keyword_text,
        max_length=150,
        help_text=article_meta_keyword_help_text,
        blank=True
    )

    content = RichTextField(
        verbose_name=article_meta_content_text
    )

    create_date = models.DateTimeField(
        verbose_name=article_create_date_text,
        default=timezone.now
    )

    last_update = models.DateTimeField(
        verbose_name=article_last_change_text,
        auto_now=True
    )


# class MeetingReservation(models.Model):
#     pass
