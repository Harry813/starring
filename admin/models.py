from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.customerSettings import Roles
from staring.models import User


# Create your models here.
class Department (models.Model):
    dep_id = models.AutoField(
        primary_key=True
    )

    dep_name = models.CharField(
        verbose_name=_("部门名称"),
        max_length=40
    )


class Staff(models.Model):
    staff_id = models.CharField(
        verbose_name=_("员工ID"),
        primary_key=True,
        max_length=50
    )

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        to=Department,
        verbose_name=_("部门"),
        on_delete=models.CASCADE
    )

    role = models.CharField(
        verbose_name=_("职位"),
        max_length=20,
        choices=Roles
    )
