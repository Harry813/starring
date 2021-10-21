from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.customerSettings import Roles, staff_tags
from staring.models import User
from staring.text import *


# Create your models here.
class Department (models.Model):
    dep_id = models.AutoField(
        primary_key=True
    )

    dep_name = models.CharField(
        verbose_name=department_dep_name_text,
        max_length=40
    )


class Staff(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True}
    )

    department = models.ForeignKey(
        to=Department,
        verbose_name=staff_department_text,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    role = models.CharField(
        verbose_name=staff_role_text,
        max_length=20,
        choices=[('', '------')] + Roles,
        blank=True
    )

    tag = models.CharField(
        verbose_name=staff_tag_text,
        max_length=20,
        choices=[('', '------')] + staff_tags,
        blank=True
    )
