from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from admin.forms import *
from admin.models import *
from admin.utils import get_admin_info
from staring.customerSettings import Languages
from staring.text import *
from staring.utils import get_basic_info


def admin_login_view(request):
    param = {
        "page_title": _("星环-管理面板登录"),
        "languages": Languages,
    }

    try:
        next_url = request.POST.get("next")
    except IndexError:
        next_url = None

    if request.user.is_authenticated():
        return HttpResponseRedirect(next_url)

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
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
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


def admin_logout_view(request):
    logout(request)
    return redirect("ADMLogin")


@login_required(login_url="ADMLogin")
def admin_index_view(request):
    param = {
        "page_title": _("星环-后台"),
        "languages": Languages,
        "user": request.user,
        "active_page": "ADMIndex",
        "info": {**get_basic_info(), **get_admin_info()}
    }

    try:
        staff_profile = Staff.objects.get(user=request.user)
        param["role"] = staff_profile.role
        param["department"] = staff_profile.department
    except Staff.DoesNotExist:
        pass

    return render(request, "admin/admin_index.html", param)


@login_required(login_url="ADMLogin")
def admin_article_index_view(request, page):
    param = {
        "page_title": _("星环-文章管理"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        "info": {**get_basic_info(), **get_admin_info()},
    }

    requirement = ["PUBLISH", "PENDING", "REJECT", "REVISED", "DRAFT"]

    p = Paginator(Article.objects.filter(status__in=requirement), 10)
    article_list = p.get_page(page)
    param["paginator"] = p
    param["article_list"] = article_list
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)

    return render(request, "admin/admin_article_index.html", param)


@login_required(login_url="ADMLogin")
def admin_article_create_view(request):
    param = {
        "page_title": _("编辑"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        "info": {**get_basic_info(), **get_admin_info()}
    }

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            # Todo: add a permission check
            return redirect("ADMArticleIndex", 1)
        else:
            param["form"] = ArticleForm()
            return render(request, "admin/admin_article_create.html", param)
    else:
        param["form"] = ArticleForm()
        return render(request, "admin/admin_article_create.html", param)


@login_required(login_url="ADMLogin")
def admin_article_edit_view(request, article_id):
    param = {
        "page_title": _("编辑"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        "info": {**get_basic_info(), **get_admin_info()}
    }

    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            # Todo: add a permission check
            return redirect("ADMArticleIndex", 1)
        else:
            param["form"] = ArticleForm(instance=article)
            return render(request, "admin/admin_article_create.html", param)
    else:
        param["form"] = ArticleForm(instance=article)
        return render(request, "admin/admin_article_create.html", param)
