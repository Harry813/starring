from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from admin.forms import AdminLoginForm
from staring.customerSettings import Languages
from staring.text import *


def index(request):
    param = {
        "page_title": _("test")
    }
    return render(request, "admin/admin_login.html", param)


def admin_login_view(request):
    param = {
        "page_title": _("星环-管理面板登录")
    }

    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        param["form"] = form

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
                    response = redirect("ADMIndex")
                    return HttpResponse("<h1>登陆成功</h1>")
                else:
                    form.add_error(None, ValidationError(UserNoPermit_text, code="UserNoPermit"))
                    return render(request, "admin/admin_login.html", param)
            else:
                form.add_error(None, ValidationError(UserNotExist_text, code="UserNotExist"))
                return render(request, "admin/admin_login.html", param)
        else:
            return render(request, "admin/admin_login.html", param)
    else:
        param["form"] = AdminLoginForm()
        return render(request, "admin/admin_login.html", param)


def admin_article_create_view(request):
    param = {
        "page_title": _("编辑"),
        "languages": Languages
    }
    return render(request, "admin/admin_template.html", param)
