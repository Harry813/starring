from django.contrib import messages
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
from admin.models import Staff
from admin.utils import get_admin_info
from customer.models import Customer
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

    if request.user.is_authenticated:
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
        **get_basic_info(),
        **get_admin_info()
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
        **get_basic_info(),
        **get_admin_info(),
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
        "page_title": _("文章创建"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            # Todo: add a permission check
            return redirect("ADMArticleIndex", 1)
        else:
            param["form"] = ArticleForm()
            return render(request, "admin/admin_article_CE.html", param)
    else:
        param["form"] = ArticleForm()
        return render(request, "admin/admin_article_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_article_edit_view(request, article_id):
    param = {
        "page_title": _("文章编辑"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        **get_basic_info(),
        **get_admin_info()
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
            return render(request, "admin/admin_article_CE.html", param)
    else:
        param["form"] = ArticleForm(instance=article)
        return render(request, "admin/admin_article_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_customer_index_view(request, page=1):
    param = {
        "page_title": _("用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    user_query = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)\
        .exclude(username="AnonymousUser")

    if request.method == "POST":
        form = CustomerSearch(request.POST)
        if form.is_valid():
            tag = form.cleaned_data.get("tag")
            if tag != "":
                user_query = user_query.filter(customer__tag=tag)

            vip = form.cleaned_data.get("vip")
            if vip != "":
                user_query = user_query.filter(customer__vip_lv=vip)

            search_type = form.cleaned_data.get("type")
            search_context = form.cleaned_data.get("detail")
            if search_type != "" and search_context is not None:
                if search_type == "UID":
                    user_query = user_query.filter(uid__icontains=search_context)
                elif search_type == "UNM":
                    user_query = user_query.filter(username__icontains=search_context)
                elif search_type == "RNM":
                    user_query = user_query.filter(name__icontains=search_context)

            param["userSearchForm"] = form
        else:
            param["userSearchForm"] = CustomerSearch(request.POST)
    else:
        param["userSearchForm"] = CustomerSearch()

    p = Paginator(user_query, 10)
    customer_list = p.get_page(page)
    param["paginator"] = p
    param["customer_list"] = customer_list
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_customer_index.html", param)


@login_required(login_url="ADMLogin")
def admin_customer_edit_view(request, customer_id):
    param = {
        "page_title": _("用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        "uid": customer_id,
        **get_basic_info(),
        **get_admin_info()
    }

    return render(request, "admin/admin_customer_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_customer_basic_edit_view(request, customer_id):
    param = {
        "page_title": _("用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    user_query = User.objects.filter(is_active=True, is_staff=False, is_superuser=False) \
        .exclude(username="AnonymousUser")
    basic_profile = get_object_or_404(user_query, uid=customer_id)
    param["customer_id"] = customer_id

    if request.method == "POST":
        basic_form = UserForm(request.POST, instance=basic_profile)
        if basic_form.is_valid():
            basic_form.update()
            return render(request, "admin/admin_customer_basic_edit.html", param)
        else:
            param["basic_form"] = UserForm(instance=basic_profile)
            return render(request, "admin/admin_customer_basic_edit.html", param)
    else:
        param["basic_form"] = UserForm(instance=basic_profile)
        return render(request, "admin/admin_customer_basic_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_customer_profile_edit_view(request, customer_id):
    param = {
        "page_title": _("用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    customer_profile = Customer.objects.get(user_id=customer_id)

    if request.method == "POST":
        customer_form = CustomerForm(request.POST, instance=customer_profile)
        if customer_form.is_valid():
            customer_form.save()
            param["customer_form"] = customer_form
            return render(request, "admin/admin_customer_profile_edit.html", param)
        else:
            param["customer_form"] = CustomerForm(instance=customer_profile)
            return render(request, "admin/admin_customer_profile_edit.html", param)
    else:
        param["customer_form"] = CustomerForm(instance=customer_profile)
        return render(request, "admin/admin_customer_profile_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_carousel_index(request):
    param = {
        "page_title": _("首页轮播管理"),
        "languages": Languages,
        "active_page": "ADMCarouselIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    pass
