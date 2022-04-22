import datetime
import time
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField

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
        blank=True,
        null=True,
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
        validators=[phone_regex],
        blank=True,
        null=True
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


class customer_articles(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="PUBLISH")


class admin_articles(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status="DELETE")


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

    # content = tinymce_models.HTMLField(
    #     verbose_name=article_content_text
    # )

    content = RichTextUploadingField(
        verbose_name=article_content_text
    )

    create_date = models.DateTimeField(
        verbose_name=article_create_date_text,
        default=timezone.now
    )

    last_update = models.DateTimeField(
        verbose_name=article_last_change_text,
        auto_now=True
    )

    view_count = models.PositiveIntegerField(
        verbose_name=article_view_count_text,
        default=0
    )

    objects = models.Manager()
    customer_visible = customer_articles()
    admin_visible = admin_articles()

    def __str__(self):
        if len(self.title) > 30:
            return self.title[:30] + "..."
        else:
            return self.title


class NewsSector(models.Model):
    name = models.CharField(
        verbose_name=newsSector_name_text,
        max_length=15,
        unique=True
    )

    max_news = models.PositiveIntegerField(
        verbose_name=newsSector_max_news_text,
        default=8
    )

    def __str__(self):
        return self.name


class News(models.Model):
    sector = models.ForeignKey(
        to=NewsSector,
        on_delete=models.CASCADE,
        verbose_name=news_sector_text
    )

    order = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        limit_choices_to={"status": "PUBLISH"},
        verbose_name=news_article_text,
    )

    title = models.CharField(
        verbose_name=news_title_text,
        max_length=60,
    )

    introduction = models.CharField(
        verbose_name=news_introduction_text,
        max_length=150,
        help_text=news_introduction_help_text,
        blank=True
    )

    img = models.ImageField(
        verbose_name=news_img_text,
        help_text=news_img_help_text,
        upload_to="news/",
        blank=True
    )

    alt = models.CharField(
        verbose_name=news_alt_text,
        help_text=news_alt_help_text,
        max_length=150,
        blank=True,
        null=True,
    )
    
    class Meta:
        unique_together = ("sector", "article")


class MeetingSlot(models.Model):
    date = models.DateField(
        verbose_name=meetingSlot_date_text
    )

    start_time = models.TimeField(
        verbose_name=meetingSlot_start_time_text
    )

    end_time = models.TimeField(
        verbose_name=meetingSlot_end_time_text
    )

    availability = models.PositiveIntegerField(
        verbose_name=meetingSlot_availability_text,
        default=1
    )

    @property
    def is_available(self):
        return self.availability > 0

    @property
    def appointment(self):
        return Appointment.objects.filter(slot=self)

    class Meta:
        unique_together = ["date", "start_time", "end_time"]


class Appointment(models.Model):
    customer = models.ForeignKey(
        to="customer.Customer",
        on_delete=models.CASCADE,
        verbose_name=appointments_customer_text
    )

    staff = models.ForeignKey(
        verbose_name=appointment_staff_text,
        to="admin.Staff",
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        to=MeetingSlot,
        on_delete=models.CASCADE,
        verbose_name=appointment_slot_text,
    )

    status = models.CharField(
        verbose_name=appointment_status_text,
        max_length=10,
        choices=meeting_status,
        default="APPLY"
    )

    created_at = models.DateTimeField(
        verbose_name=appointment_create_text,
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=appointment_update_text,
        auto_now=True,
    )


class MeetingUpdate(models.Model):
    appointment = models.ForeignKey(
        to=Appointment,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=150
    )

    attachment = models.FileField(
        upload_to="MeetingRecords",
        blank=True,
        null=True
    )

    message = RichTextUploadingField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_update = models.DateTimeField(
        auto_now=True
    )

    def time_diff(self):
        diff = datetime.datetime.now().replace(tzinfo=None) - self.created_at.replace(tzinfo=None)
        diff = diff.total_seconds()
        if diff < 3600:
            return f"{int(divmod(diff, 60)[0])} " + _("分钟")
        elif 3600 <= diff < 86400:
            return f"{int(divmod(diff, 3600)[0])} " + _("小时")
        else:
            return f"{int(divmod(diff, 86400)[0])} " + _("天")

    class Meta:
        ordering = ["last_update"]


class NavigatorSector(models.Model):
    name = models.CharField(
        verbose_name=navi_sector_name_text,
        max_length=30,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=navi_sector_order_text,
    )

    def __str__(self):
        return f"{self.order}. {self.name}"

    class Meta:
        ordering = ["order"]


class NavigatorItem(models.Model):
    sector = models.ForeignKey(
        verbose_name=navi_item_sector_text,
        to=NavigatorSector,
        on_delete=models.CASCADE
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=navi_item_order_text,
    )

    level = models.IntegerField(
        verbose_name=navi_item_level_text,
        choices=navigator_item_level
    )

    name = models.CharField(
        verbose_name=navi_item_name_text,
        max_length=30,
    )

    type = models.CharField(
        verbose_name=navi_item_type_text,
        choices=link_type,
        max_length=10,
    )

    url = models.CharField(
        verbose_name=navi_item_url_text,
        max_length=150,
        blank=True,
        null=True,
        help_text=navi_item_url_help_text
    )

    article = models.ForeignKey(
        verbose_name=navi_item_article_text,
        to=Article,
        limit_choices_to={'status': 'PUBLISH'},
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=navi_item_article_help_text
    )

    def get_indentation(self):
        return "----" * self.level

    class Meta:
        ordering = ["sector", "order"]


class IndexListSector(models.Model):
    name = models.CharField(
        verbose_name=index_list_sector_name,
        max_length=15,
    )

    def __str__(self):
        return self.name


class IndexListItem(models.Model):
    name = models.CharField(
        verbose_name=index_list_item_name_text,
        max_length=15,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=index_list_item_order_text
    )

    sector = models.ForeignKey(
        verbose_name=index_list_item_sector_text,
        to=IndexListSector,
        on_delete=models.CASCADE
    )

    type = models.CharField(
        verbose_name=navi_item_type_text,
        choices=link_type,
        max_length=10,
    )

    url = models.CharField(
        verbose_name=navi_item_url_text,
        max_length=150,
        blank=True,
        null=True,
        help_text=navi_item_url_help_text,
        default="#"
    )

    article = models.ForeignKey(
        verbose_name=navi_item_article_text,
        to=Article,
        limit_choices_to={'status': 'PUBLISH'},
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=navi_item_article_help_text
    )

    def link(self):
        if self.type == "URL":
            return self.url
        elif self.type == "ARTICLE":
            return reverse("article", args=[self.article.id])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sector", "order"]


class IndexSidebarItem(models.Model):
    order = models.PositiveSmallIntegerField(
        # verbose_name=navi_item_order_text,
    )

    display = models.CharField(
        # verbose_name=navi_item_name_text,
        max_length=30,
    )

    type = models.CharField(
        # verbose_name=navi_item_type_text,
        choices=link_type,
        max_length=10,
    )

    url = models.CharField(
        verbose_name=navi_item_url_text,
        max_length=150,
        blank=True,
        null=True,
        # help_text=navi_item_url_help_text
    )

    article = models.ForeignKey(
        # verbose_name=navi_item_article_text,
        to=Article,
        limit_choices_to={'status': 'PUBLISH'},
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        # help_text=navi_item_article_help_text
    )

    class Meta:
        ordering = ["order"]


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    customer = models.ForeignKey(
        to="customer.Customer",
        on_delete=models.CASCADE,
    )
    
    payment_method = models.CharField(
        max_length=10,
        choices=payment_method
    )

    def __str__(self):
        return str(self.id).replace("-", "")


class TransactionItem(models.Model):
    description = models.CharField(
        max_length=150
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
