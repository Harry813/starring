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
import staring.crs_setting as crs
from staring.utils import *

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

    def get_uid_as_string (self):
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

    def get_display_name (self):
        if self.name:
            return self.name
        elif self.username:
            return self.username

    dob = models.DateField(
        verbose_name=user_dob_text,
        blank=True,
        null=True,
    )

    def format_dob (self):
        if self.dob:
            return self.dob.strftime("%Y-%m-%d")
        else:
            return None

    def get_age (self):
        age = datetime.date.today().year - self.dob.year
        return age

    email = models.EmailField(
        verbose_name=email_text,
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
        upload_to="avatar/",
        blank=True
    )

    def get_phone (self):
        phone = "+{}-{}".format(self.countryCode, self.tele)
        return phone

    # hidden, can only access by admins
    is_active = models.BooleanField(
        verbose_name=user_active_text,
        default=True,
        help_text=user_active_help_text,
    )

    date_joined = models.DateTimeField(
        verbose_name=user_date_join_text,
        auto_now_add=True,
    )

    last_change = models.DateTimeField(
        verbose_name=user_last_change_text,
        auto_now=True
    )

    def __str__ (self):
        return self.get_display_name()


class customer_articles(models.Manager):
    def get_queryset (self):
        return super().get_queryset().filter(status="PUBLISH")


class admin_articles(models.Manager):
    def get_queryset (self):
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

    def __str__ (self):
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

    def __str__ (self):
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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    start_datetime = models.DateTimeField(
        verbose_name=meetingSlot_start_time_text,
    )

    end_datetime = models.DateTimeField(
        verbose_name=meetingSlot_end_time_text,
    )

    status = models.CharField(
        verbose_name=meetingSlot_status_text,
        max_length=10,
        choices=slot_status,
        default="AVAILABLE",
    )

    @property
    def date (self):
        return self.start_datetime.date()

    @property
    def start_time (self):
        return self.start_datetime.time()

    @property
    def end_time (self):
        return self.end_datetime.time()

    @property
    def duration (self):
        delta = (self.end_datetime - self.start_datetime).total_seconds()
        m = delta // 60
        msg = f"{m}m"
        return msg

    def __str__ (self):
        return f"{self.date} {self.start_time}-{self.end_time}"

    @property
    def is_available (self):
        return self.status == "AVAILABLE"

    @property
    def appointment (self):
        return Appointment.objects.filter(slot=self)

    @property
    def as_property (self):
        s = {
            "id": self.id,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
        }
        return s

    class Meta:
        unique_together = ["start_datetime", "end_datetime"]
        ordering = ["start_datetime"]


class Appointment(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
    )

    customer = models.ForeignKey(
        to="customer.Customer",
        on_delete=models.CASCADE,
        verbose_name=appointments_customer_text
    )

    title_prefix = models.CharField(
        max_length=5,
        choices=title_prefix,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=appointment_name_text,
        help_text=appointment_name_help_text,
    )

    email = models.EmailField(
        verbose_name=email_text,
    )

    staff = models.ForeignKey(
        verbose_name=appointment_staff_text,
        to="admin.Staff",
        on_delete=models.CASCADE,
        limit_choices_to={'is_consultant': True},
        blank=True,
        null=True,
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

    @property
    def price(self):
        price = Decimal(0.00)
        if self.customer.vip_lv in [2, 3]:
            price += Decimal(100)
        else:
            price += Decimal(200)
        return price

    def __str__ (self):
        return _("预约: %(id)s-[%(name)s]-{%(time)s}") % {
            "id": str(self.id)[-8:].capitalize(),
            "name": str(self.name).strip(" "),
            "time": f"{self.slot.date} {self.slot.start_time}-{self.slot.end_time}"
        }


class MeetingUpdate(models.Model):
    appointment = models.ForeignKey(
        to=Appointment,
        on_delete=models.CASCADE,
        verbose_name=update_appointment_text,
    )

    title = models.CharField(
        max_length=150,
        verbose_name=update_title_text,
    )

    attachment = models.FileField(
        upload_to="MeetingRecords/",
        blank=True,
        null=True,
        verbose_name=update_attachment_text
    )

    message = RichTextUploadingField(
        blank=True,
        null=True,
        verbose_name=update_message_text
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    last_update = models.DateTimeField(
        auto_now=True
    )

    def time_diff (self):
        diff = datetime.datetime.now().replace(tzinfo=None) - self.created_at.replace(tzinfo=None)
        diff = diff.total_seconds()
        if diff < 60:
            return _("刚刚")
        elif 60 <= diff < 3600:
            return f"{int(diff // 60)} " + _("分钟前")
        elif 3600 <= diff < 86400:
            return f"{int(diff // 3600)} " + _("小时前")
        else:
            return f"{int(diff // 86400)} " + _("天前")

    class Meta:
        ordering = ["last_update"]

    @property
    def is_pic (self):
        # .split(".")[-1] in [".png", ".jpg", ".gif", ".tif", ".tiff", "jpeg"]
        return self.attachment.name


class NavigatorSector(models.Model):
    name = models.CharField(
        verbose_name=navi_sector_name_text,
        max_length=30,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=navi_sector_order_text,
    )

    def __str__ (self):
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

    def get_indentation (self):
        return "----" * self.level

    class Meta:
        ordering = ["sector", "order"]


class IndexListSector(models.Model):
    name = models.CharField(
        verbose_name=index_list_sector_name,
        max_length=15,
    )

    def __str__ (self):
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

    def link (self):
        if self.type == "URL":
            return self.url
        elif self.type == "ARTICLE":
            return reverse("article", args=[self.article.id])

    def __str__ (self):
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

    def __str__ (self):
        return str(self.id).replace("-", "")


class TransactionItem(models.Model):
    description = models.CharField(
        max_length=150
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class CRS(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    customer = models.ForeignKey(
        to="customer.Customer",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # Section A: Core / human capital factors
    marriage_status = models.IntegerField(
        verbose_name=crs.marriage_status_text,
        choices=crs.marriage_status,
        blank=True,
        null=True
    )

    @property
    def marriage_class (self):
        return [0, 1][self.marriage_status in [1, 2, 3]]

    age_group = models.IntegerField(
        verbose_name=crs.age_group_text,
        choices=crs.age_group,
        blank=True,
        null=True,
    )

    @property
    def is_age_group_valid (self):
        return self.age_group >= 0

    @property
    def age_group_score (self):
        return crs.age_group_score[self.marriage_class][self.age_group]

    @property
    def age_final_score (self):
        score = self.age_group_score
        if self.marriage_class == 0:
            if score >= 110:
                return 110
            else:
                return score
        elif self.marriage_class == 1:
            if score >= 100:
                return 100
            else:
                return score
        else:
            return 0

    education_lv = models.IntegerField(
        verbose_name=crs.education_lv_text,
        choices=crs.education_lv,
        blank=True,
        null=True,
    )

    @property
    def education_lv_score (self):
        return crs.education_lv_score[self.marriage_class][self.education_lv]

    @property
    def education_lv_classification (self):
        education_lv = self.education_lv
        if education_lv in [0, 1]:
            return 0
        elif education_lv in [2, 3, 4]:
            return 1
        elif education_lv in [5, 6, 7]:
            return 2

    education_canadian = models.BooleanField(
        verbose_name=crs.education_canadian_text,
        choices=crs.boolean_general,
        blank=True,
        null=True,
    )

    @property
    def education_canadian_bonus_score (self):
        education_lv = self.education_lv
        education_canadian = self.education_canadian
        if education_canadian == 1:
            if education_lv in [2, 3]:
                return 15
            elif education_lv in [4, 5, 6, 7]:
                return 30

    @property
    def education_final_score (self):
        score = sum([self.education_lv_score, self.education_canadian_bonus_score])
        if self.marriage_class == 0:
            if score >= 150:
                return 150
            else:
                return score
        elif self.marriage_class == 1:
            if score >= 140:
                return 140
            else:
                return score
        else:
            return 0

    valid_first_language = models.BooleanField(
        verbose_name=crs.education_canadian_text,
        choices=crs.boolean_general,
        blank=True,
        null=True,
    )

    first_language_test = models.IntegerField(
        verbose_name=crs.first_language_test_text,
        choices=crs.language_test,
        blank=True,
        null=True
    )

    first_language_listening = models.DecimalField(
        verbose_name=crs.first_listening_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def first_language_listening_CLB (self):
        return get_subject_CLB(self.first_language_test, "L", self.first_language_listening)

    @property
    def first_language_listening_score (self):
        return get_first_language_score(self.marriage_class, self.first_language_listening_CLB)

    first_language_speaking = models.DecimalField(
        verbose_name=crs.first_speaking_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def first_language_speaking_CLB (self):
        return get_subject_CLB(self.first_language_test, "S", self.first_language_speaking)

    @property
    def first_language_speaking_score (self):
        return get_first_language_score(self.marriage_class, self.first_language_speaking_CLB)

    first_language_reading = models.DecimalField(
        verbose_name=crs.first_reading_text,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        max_digits=4,
        blank=True,
        null=True
    )

    @property
    def first_language_reading_CLB (self):
        return get_subject_CLB(self.first_language_test, "R", self.first_language_reading)

    @property
    def first_language_reading_score (self):
        return get_first_language_score(self.marriage_class, self.first_language_reading_CLB)

    first_language_writing = models.DecimalField(
        verbose_name=crs.first_writing_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def first_language_writing_CLB (self):
        return get_subject_CLB(self.first_language_test, "W", self.first_language_writing)

    @property
    def first_language_writing_score (self):
        return get_first_language_score(self.marriage_class, self.first_language_writing_CLB)

    @property
    def first_language_CLB (self):
        return min([
            self.first_language_listening_CLB,
            self.first_language_speaking_CLB,
            self.first_language_reading_CLB,
            self.first_language_writing_CLB
        ])

    @property
    def first_language_CLB_classification (self):
        if self.first_language_CLB < 7:
            return 0
        elif self.first_language_CLB >= 7 and any([self.first_language_listening_CLB >= 9,
                                                   self.first_language_speaking_CLB >= 9,
                                                   self.first_language_reading_CLB >= 9,
                                                   self.first_language_writing_CLB >= 9]):
            return 1
        elif self.first_language_CLB >= 9:
            return 2
        else:
            return -1

    @property
    def first_language_score (self):
        return sum([self.first_language_listening_score, self.first_language_speaking_score,
                    self.first_language_reading_score, self.first_language_writing_score])

    @property
    def first_language_final_score (self):
        score = self.first_language_score
        if score >= 136:
            return 136
        else:
            return score

    valid_second_language = models.BooleanField(
        verbose_name=crs.valid_second_language_test_text,
        choices=crs.boolean_general,
        blank=True,
        null=True,
    )

    second_language_test = models.IntegerField(
        verbose_name=crs.first_language_test_text,
        choices=crs.language_test,
        blank=True,
        null=True
    )

    second_language_listening = models.DecimalField(
        verbose_name=crs.second_listening_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def second_language_listening_CLB (self):
        if self.valid_second_language:
            return get_subject_CLB(self.second_language_test, "L", self.second_language_listening)
        else:
            return 0

    @property
    def second_language_listening_score (self):
        return get_second_language_score(self.second_language_listening_CLB)

    second_language_speaking = models.DecimalField(
        verbose_name=crs.second_speaking_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def second_language_speaking_CLB (self):
        if self.valid_second_language:
            return get_subject_CLB(self.second_language_test, "S", self.second_language_speaking)
        else:
            return 0

    @property
    def second_language_speaking_score (self):
        return get_second_language_score(self.second_language_speaking_CLB)

    second_language_reading = models.DecimalField(
        verbose_name=crs.second_reading_text,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        max_digits=4,
        blank=True,
        null=True
    )

    @property
    def second_language_reading_CLB (self):
        if self.valid_second_language:
            return get_subject_CLB(self.second_language_test, "R", self.second_language_reading)
        else:
            return 0

    @property
    def second_language_reading_score (self):
        return get_second_language_score(self.second_language_reading_CLB)

    second_language_writing = models.DecimalField(
        verbose_name=crs.second_writing_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def second_language_writing_CLB (self):
        if self.valid_second_language:
            return get_subject_CLB(self.second_language_test, "W", self.second_language_writing)
        else:
            return 0

    @property
    def second_language_writing_score (self):
        return get_second_language_score(self.second_language_writing_CLB)

    @property
    def second_language_CLB (self):
        return min([
            self.second_language_listening_CLB,
            self.second_language_speaking_CLB,
            self.second_language_reading_CLB,
            self.second_language_writing_CLB
        ])

    @property
    def second_language_CLB_classification (self):
        if self.second_language_CLB < 7:
            return 0
        elif self.second_language_CLB >= 7 and any([self.second_language_listening_CLB >= 9,
                                                    self.second_language_speaking_CLB >= 9,
                                                    self.second_language_reading_CLB >= 9,
                                                    self.second_language_writing_CLB >= 9]):
            return 1
        elif self.second_language_CLB >= 9:
            return 2
        else:
            return -1

    @property
    def second_language_score (self):
        return sum([self.second_language_listening_score, self.second_language_speaking_score,
                    self.second_language_reading_score, self.second_language_writing_score])

    @property
    def second_language_final_score (self):
        score = self.second_language_score
        if self.marriage_class == 0:
            if score >= 24:
                return 24
            else:
                return score
        elif self.marriage_class == 1:
            if score >= 22:
                return 22
            else:
                return score

    @property
    def language_final_score (self):
        score = self.first_language_final_score + self.second_language_final_score
        if self.marriage_class == 0:
            if score >= 160:
                return 160
            else:
                return score
        elif self.marriage_class == 1:
            if score >= 150:
                return 150
            else:
                return score
        else:
            return 0

    work_experience = models.IntegerField(
        verbose_name=crs.work_experience_text,
        choices=crs.work_experience,
        blank=True,
        null=True
    )

    @property
    def is_work_experience_valid (self):
        return self.work_experience != 0

    @property
    def work_experience_final_score (self):
        marriage_class = self.marriage_class
        score = crs.work_experience_score[marriage_class][self.work_experience]
        if marriage_class == 0:
            if score >= 80:
                return 80
            else:
                return score
        elif marriage_class == 1:
            if score >= 70:
                return 70
            else:
                return score
        else:
            return 0

    NOC = models.CharField(
        verbose_name=crs.NOC_text,
        choices=crs.noc,
        max_length=4,
        blank=True,
        null=True,
    )

    foreign_work_experience = models.IntegerField(
        verbose_name=crs.foreign_work_experience_text,
        choices=crs.foreign_work_experience,
        blank=True,
        null=True
    )

    @property
    def is_foreign_work_experience_valid (self):
        return self.foreign_work_experience != 0

    @property
    def section_A_total_score (self):
        return sum([
            self.age_final_score,
            self.education_final_score,
            self.language_final_score,
            self.work_experience_final_score
        ])

    # Section B: Spouse or common-law partner factors
    partner_education_lv = models.IntegerField(
        verbose_name=crs.education_lv_text,
        choices=crs.education_lv,
        blank=True,
        null=True,
    )

    @property
    def partner_education_lv_score (self):
        marriage_class = self.marriage_class
        if marriage_class == 1:
            return crs.partner_education_lv_score[self.partner_education_lv]
        else:
            return 0

    valid_partner_language = models.BooleanField(
        verbose_name=crs.valid_partner_language_test_text,
        choices=crs.boolean_general,
        blank=True,
        null=True,
    )

    partner_language_test = models.IntegerField(
        verbose_name=crs.partner_language_test_text,
        choices=crs.language_test,
        blank=True,
        null=True
    )

    partner_language_listening = models.DecimalField(
        verbose_name=crs.partner_listening_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def partner_language_listening_CLB (self):
        return get_subject_CLB(self.partner_language_test, "L", self.partner_language_listening)

    @property
    def partner_language_listening_score (self):
        return get_partner_language_score(self.partner_language_listening_CLB)

    partner_language_speaking = models.DecimalField(
        verbose_name=crs.partner_speaking_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def partner_language_speaking_CLB (self):
        return get_subject_CLB(self.partner_language_test, "S", self.partner_language_speaking)

    @property
    def partner_language_speaking_score (self):
        return get_partner_language_score(self.partner_language_speaking_CLB)

    partner_language_reading = models.DecimalField(
        verbose_name=crs.partner_reading_text,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        max_digits=4,
        blank=True,
        null=True
    )

    @property
    def partner_language_reading_CLB (self):
        return get_subject_CLB(self.partner_language_test, "R", self.partner_language_reading)

    @property
    def partner_language_reading_score (self):
        return get_partner_language_score(self.partner_language_reading_CLB)

    partner_language_writing = models.DecimalField(
        verbose_name=crs.partner_writing_text,
        decimal_places=1,
        max_digits=4,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    @property
    def partner_language_writing_CLB (self):
        return get_subject_CLB(self.partner_language_test, "W", self.partner_language_writing)

    @property
    def partner_language_writing_score (self):
        return get_partner_language_score(self.partner_language_writing_CLB)

    @property
    def partner_language_CLB (self):
        return min([
            self.partner_language_listening_CLB,
            self.partner_language_speaking_CLB,
            self.partner_language_reading_CLB,
            self.partner_language_writing_CLB
        ])

    @property
    def partner_language_score (self):
        return sum([
            self.partner_language_listening_CLB,
            self.partner_language_speaking_CLB,
            self.partner_language_reading_CLB,
            self.partner_language_writing_CLB
        ])

    @property
    def partner_language_final_score (self):
        if self.marriage_class == 1:
            score = self.partner_language_score
            if score >= 20:
                return 20
            else:
                return score
        else:
            return 0

    partner_work_experience = models.IntegerField(
        verbose_name=crs.partner_work_experience_text,
        choices=crs.work_experience,
        blank=True,
        null=True
    )

    @property
    def partner_work_experience_score (self):
        if self.marriage_class == 1:
            return crs.partner_work_experience_score[self.partner_work_experience]
        else:
            return 0

    @property
    def partner_total_final_score (self):
        if self.marriage_class == 1:
            score = sum([
                self.partner_education_lv_score,
                self.partner_language_final_score,
                self.partner_work_experience_score
            ])
            if score >= 40:
                return 40
            else:
                return score
        else:
            return 0

    # Section C: Additional points
    valid_certificate = models.BooleanField(
        verbose_name=crs.valid_certificate_text,
        choices=crs.boolean_general,
        blank=True,
        null=True
    )

    valid_job_offer = models.BooleanField(
        verbose_name=crs.valid_job_offer_text,
        choices=crs.boolean_general,
        blank=True,
        null=True
    )

    valid_nomination = models.BooleanField(
        verbose_name=crs.valid_nomination_text,
        choices=crs.boolean_general,
        blank=True,
        null=True
    )

    @property
    def valid_nomination_score (self):
        return [0, 600][self.valid_nomination]

    valid_relatives_citizen = models.BooleanField(
        verbose_name=crs.valid_relatives_citizen_text,
        choices=crs.boolean_general,
        blank=True,
        null=True
    )

    @property
    def arranged_noc (self):
        if self.NOC == "00":
            return 200
        elif self.NOC in ["0", "A", "B"]:
            return 50
        else:
            return 0

    @property
    def valid_relatives_citizen_score (self):
        return [0, 15][self.valid_relatives_citizen]

    @property
    def valid_French_with_English (self):
        listening_score = 0
        speaking_score = 0
        reading_score = 0
        writing_score = 0
        english_listening_score = 0
        english_speaking_score = 0
        english_reading_score = 0
        english_writing_score = 0
        if self.first_language_test in [2, 3]:
            listening_score = self.first_language_listening_CLB
            reading_score = self.first_language_reading_CLB
            speaking_score = self.first_language_speaking_CLB
            writing_score = self.first_language_writing_CLB
            if self.valid_second_language:
                english_listening_score = self.second_language_listening_CLB
                english_reading_score = self.second_language_reading_CLB
                english_speaking_score = self.second_language_speaking_CLB
                english_writing_score = self.second_language_writing_CLB
        elif self.second_language_test in [2, 3]:
            listening_score = self.second_language_listening_CLB
            reading_score = self.second_language_reading_CLB
            speaking_score = self.second_language_speaking_CLB
            writing_score = self.second_language_writing_CLB

            english_writing_score = self.first_language_writing_CLB
            english_speaking_score = self.first_language_speaking_CLB
            english_reading_score = self.first_language_reading_CLB
            english_listening_score = self.first_language_listening_CLB

        min_french = min(listening_score, speaking_score, reading_score, writing_score)
        min_english = min(english_listening_score, english_reading_score, english_speaking_score, english_writing_score)

        if min_french >= 7:
            if min_english >= 5:
                return 50
            else:
                return 25
        else:
            return 0

    eligible = models.BooleanField(
        verbose_name=crs.eligible_text,
        choices=crs.boolean_general,
        blank=True,
        null=True,
    )

    @property
    def additional_final_score (self):
        score = sum([
            self.valid_nomination_score,
            self.valid_relatives_citizen_score,
            self.valid_French_with_English,
            self.arranged_noc,
        ])
        if score >= 600:
            return 600
        else:
            return score

    # Section D: Skill Transferability factors
    @property
    def language_proficiency_with_degree (self):
        education_lv_classification = self.education_lv_classification
        clb_classification = self.first_language_CLB_classification

        if clb_classification == 0 or education_lv_classification == 0:
            return 0
        elif clb_classification == 1:
            if education_lv_classification == 1:
                return 13
            elif education_lv_classification == 2:
                return 25
        elif clb_classification == 2:
            if education_lv_classification == 1:
                return 25
            elif education_lv_classification == 2:
                return 50
        else:
            return 0

    @property
    def canada_work_experience_with_degree (self):
        education_lv = self.education_lv
        work_experience = self.work_experience

        if work_experience == 0:
            return 0
        elif work_experience == 1:
            if education_lv in [0, 1]:
                return 0
            elif education_lv in [2, 3, 4]:
                return 13
            elif education_lv in [5, 6, 7]:
                return 25
        elif work_experience >= 2:
            if education_lv in [0, 1]:
                return 0
            elif education_lv in [2, 3, 4]:
                return 25
            elif education_lv in [5, 6, 7]:
                return 50

    @property
    def foreign_work_experience_with_language_proficiency (self):
        foreign_work_experience = self.foreign_work_experience
        if self.first_language_CLB_classification == 1:
            if foreign_work_experience in [1, 2]:
                return 13
            elif foreign_work_experience == 3:
                return 25
            else:
                return 0
        elif self.first_language_CLB_classification == 2:
            if foreign_work_experience in [1, 2]:
                return 25
            elif foreign_work_experience == 3:
                return 50
            else:
                return 0
        else:
            return 0

    @property
    def foreign_work_experience_with_canada_work_experience (self):
        # todo: 需要更改
        return 0

    @property
    def certified_qualification_with_degree (self):
        if self.valid_certificate:
            if self.first_language_CLB >= 7 or self.second_language_CLB >= 7:
                return 50
            elif 7 >= self.first_language_CLB >= 5 or 7 >= self.second_language_CLB >= 5:
                return 25
            else:
                return 0
        else:
            return 0

    @property
    def skill_transferability_final_score (self):
        score = sum([
            self.language_proficiency_with_degree,
            self.canada_work_experience_with_degree,
            self.foreign_work_experience_with_language_proficiency,
            self.foreign_work_experience_with_canada_work_experience,
            self.certified_qualification_with_degree,
        ])
        if score >= 100:
            return 100
        else:
            return score

    def save (self, **kwargs):
        if self.is_age_group_valid and self.is_work_experience_valid and self.is_foreign_work_experience_valid:
            self.eligible = True
        else:
            self.eligible = False
        super().save(**kwargs)
