from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from admin.forms import *
from admin.models import *
from staring.customerSettings import Languages
from staring.text import *


def admin_login_view(request):
    param = {
        "page_title": _("星环-管理面板登录"),
        "languages": Languages,
    }

    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            paswd = form.cleaned_data.get("password")

            user = authenticate(
                request=request,
                username=username,
                password=paswd
            )
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect("ADMIndex")
                else:
                    form.add_error(None, ValidationError(UserNoPermit_text, code="UserNoPermit"))
            else:
                form.add_error(None, ValidationError(UserNotExist_text, code="UserNotExist"))

            param["form"] = form
            return render(request, "admin/admin_login.html", param)

        else:
            param["form"] = form
            return render(request, "admin/admin_login.html", param)
    else:
        param["form"] = AdminLoginForm()
        return render(request, "admin/admin_login.html", param)


@login_required(login_url="ADMLogin")
def admin_index_view(request):
    param = {
        "page_title": _("星环-后台"),
        "languages": Languages,
        "user": request.user,
    }

    try:
        staff_profile = Staff.objects.get(user=request.user)
        param["role"] = staff_profile.role
        param["department"] = staff_profile.department
    except Staff.DoesNotExist as e:
        pass

    return render(request, "admin/admin_index.html", param)


@login_required(login_url="ADMLogin")
def admin_article_create_view(request):
    param = {
        "page_title": _("编辑"),
        "languages": Languages,
    }

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            pass

    return render(request, "admin/admin_template.html", param)
