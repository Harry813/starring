import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n
from django.views.decorators.csrf import csrf_exempt

from admin.forms import *
from admin.models import Staff
from admin.utils import get_admin_info
from customer.models import Customer
from staring.customerSettings import Languages
from staring.settings import MEDIA_ROOT, MEDIA_URL, DOMAIN_NAME
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

    articles = Article.objects.all()

    if request.method == "POST":
        form = ArticleSearchForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            if status != "":
                articles = articles.filter(status=status)

            lv_require = form.cleaned_data.get("lv_require")
            if lv_require < 0:
                articles = articles.filter(lv_require__lte=lv_require)

            search_type = form.cleaned_data.get("search_type")
            detail = form.cleaned_data.get("detail")
            if search_type != "" and detail != "":
                if search_type == "TITLE":
                    articles = articles.filter(title__icontains=detail)
                elif search_type == "CONTENT":
                    articles = articles.filter(content__icontains=detail)
                elif search_type == "TC":
                    articles = articles.filter(Q(title__icontains=detail) | Q(content__icontains=detail))
                elif search_type == "AUTHOR":
                    articles = articles.filter(author__icontains=detail)
                elif search_type == "KEYWORD":
                    articles = articles.filter(keywords__icontains=detail)
                elif search_type == "DESCRIPTION":
                    articles = articles.filter(description__icontains=detail)
        else:
            form = ArticleSearchForm(request.POST)
    else:
        form = ArticleSearchForm()

    p = Paginator(articles, 10)
    article_list = p.get_page(page)
    param["paginator"] = p
    param["article_list"] = article_list
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    param["SearchForm"] = form

    return render(request, "admin/admin_article_index.html", param)


@login_required(login_url="ADMLogin")
def admin_article_create_view(request):
    param = {
        "page_title": _("星环-文章创建"),
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
        "page_title": _("星环-文章编辑"),
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
        "page_title": _("星环-用户管理"),
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
        "page_title": _("星环-用户管理"),
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
        "page_title": _("星环-用户管理"),
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
            return render(request, "admin/admin_user_basic_edit.html", param)
        else:
            param["basic_form"] = UserForm(instance=basic_profile)
            return render(request, "admin/admin_user_basic_edit.html", param)
    else:
        param["basic_form"] = UserForm(instance=basic_profile)
        return render(request, "admin/admin_user_basic_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_customer_profile_edit_view(request, customer_id):
    param = {
        "page_title": _("星环-用户管理"),
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
def admin_staff_index_view(request, page=1):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        **get_basic_info(),
        **get_admin_info()
    }

    user_query = User.objects.filter(is_active=True).filter(Q(is_staff=True) | Q(is_superuser=True)).\
        exclude(username="AnonymousUser")

    if request.method == "POST":
        form = StaffSearch(request.POST)
        if form.is_valid():
            tag = form.cleaned_data.get("tag")
            if tag != "":
                user_query = user_query.filter(staff__tag=tag)

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
            param["userSearchForm"] = StaffSearch(request.POST)
    else:
        param["userSearchForm"] = StaffSearch()

    p = Paginator(user_query, 10)
    staff_list = p.get_page(page)
    param["paginator"] = p
    param["staff_list"] = staff_list
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_staff_index.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_edit_view(request, staff_id):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        "uid": staff_id,
        **get_basic_info(),
        **get_admin_info()
    }

    return render(request, "admin/admin_staff_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_basic_edit_view(request, staff_id):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        **get_basic_info(),
        **get_admin_info()
    }

    user_query = User.objects.filter(is_active=True).filter(Q(is_staff=True) | Q(is_superuser=True))\
        .exclude(username="AnonymousUser")
    basic_profile = get_object_or_404(user_query, uid=staff_id)
    param["user_id"] = staff_id

    if request.method == "POST":
        basic_form = UserForm(request.POST, instance=basic_profile)
        if basic_form.is_valid():
            basic_form.update()
            return render(request, "admin/admin_user_basic_edit.html", param)
        else:
            param["basic_form"] = UserForm(instance=basic_profile)
            return render(request, "admin/admin_user_basic_edit.html", param)
    else:
        param["basic_form"] = UserForm(instance=basic_profile)
        return render(request, "admin/admin_user_basic_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_profile_edit_view(request, staff_id):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        **get_basic_info(),
        **get_admin_info()
    }

    staff_profile = Staff.objects.get_or_create(user_id=staff_id, defaults={'user': User.objects.get(uid=staff_id)})
    if request.method == "POST":
        staff_form = StaffForm(request.POST, instance=staff_profile)
        if staff_form.is_valid():
            staff_form.save()
            param["staff_form"] = staff_form
            return render(request, "admin/admin_staff_profile_edit.html", param)
        else:
            param["staff_form"] = staff_form
            return render(request, "admin/admin_staff_profile_edit.html", param)
    else:
        param["staff_form"] = StaffForm()
        return render(request, "admin/admin_staff_profile_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_create_view(request):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = StaffCreateForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1"),
                email=form.cleaned_data.get("email")
            )
            u.name = form.cleaned_data.get("name")
            u.dob = form.cleaned_data.get("dob")
            u.countryCode = form.cleaned_data.get("code")
            u.tele = form.cleaned_data.get("tele")
            u.is_staff = True
            s = Staff.objects.create(
                user=u
            )
            u.save()
            s.save()
            return redirect("ADMStaffIndex", 1)
    else:
        form = StaffCreateForm()
    param["form"] = form
    return render(request, "admin/admin_staff_create.html", param)


@login_required(login_url="ADMLogin")
def admin_news_sector_index_view(request):
    param = {
        "page_title": _("星环-新闻分区"),
        "languages": Languages,
        "active_page": "ADMNewsSectorIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = NewsSectorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = NewsSectorForm(request.POST)
    else:
        form = NewsSectorForm()

    param["form"] = form

    param["sector_list"] = NewsSector.objects.all()
    param["count"] = len(NewsSector.objects.all())
    return render(request, 'admin/admin_sector.html', param)


@login_required(login_url="ADMLogin")
def admin_news_sector_edit_view(request, sid):
    param = {
        "page_title": _("星环-新闻分区管理"),
        "languages": Languages,
        "active_page": "ADMNewsSectorIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    sector = NewsSector.objects.get(id=sid)

    if request.method == "POST":
        form = NewsSectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            return redirect("ADMNewsSectorIndex")
        else:
            form = NewsSectorForm(request.POST, instance=sector)
    else:
        form = NewsSectorForm(instance=sector)

    param["form"] = form
    return render(request, 'admin/admin_sector_edit.html', param)


@login_required(login_url="ADMLogin")
def admin_news_index_view(request):
    param = {
        "page_title": _("星环-新闻管理"),
        "languages": Languages,
        "active_page": "ADMNewsIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    news = News.objects.all()

    if request.method == "POST":
        form = NewsSearchForm(request.POST)
        if form.is_valid():
            sector = form.cleaned_data.get("sector")
            if sector != "":
                news = News.objects.filter(sector=sector)
        else:
            form = NewsSearchForm(request.POST)
    else:
        form = NewsSearchForm()

    param["news"] = news
    param["form"] = form

    return render(request, "admin/admin_news_index.html", param)


@login_required(login_url="ADMLogin")
def admin_news_create_view(request):
    param = {
        "page_title": _("星环-新闻创建"),
        "languages": Languages,
        "active_page": "ADMNewsIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ADMNewsIndex")
        else:
            form = NewsForm(request.POST)
    else:
        form = NewsForm()

    param["form"] = form
    return render(request, "admin/admin_news_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_news_edit_view(request, nid):
    param = {
        "page_title": _("星环-新闻编辑"),
        "languages": Languages,
        "active_page": "ADMNewsIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    news = News.objects.get(id=nid)

    if request.method == "POST":
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect("ADMNewsIndex")
        else:
            form = NewsForm(request.POST, instance=news)
    else:
        form = NewsForm(instance=news)

    param["form"] = form
    return render(request, "admin/admin_news_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_slot_index_view(request, page):
    param = {
        "page_title": _("星环-日程管理"),
        "languages": Languages,
        "active_page": "ADMSlotIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    timeslots = MeetingSlot.objects.filter(date__gte=datetime.datetime.today())

    p = Paginator(timeslots, 10)
    timeslots = p.get_page(page)
    param["paginator"] = p
    param["timeslots"] = timeslots
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_slots.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_sector_index_view(request):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        "sectors": NavigatorSector.objects.all(),
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = NaviSectorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = NaviSectorForm(request.POST)
    else:
        form = NaviSectorForm()

    param["form"] = form

    return render(request, "admin/admin_navi_sector_index.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_sector_delete(request, secid):
    try:
        NavigatorSector.objects.get(id=secid).delete()
    except ValidationError:
        pass
    return redirect("ADMNaviSectorIndex")


@login_required(login_url="ADMLogin")
def admin_navi_item_index_view(request, secid):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = NavigatorSector.objects.get(id=secid)

    if request.method == "POST":
        form = NaviSectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
        else:
            form = NaviSectorForm(request.POST, instance=sector)
    else:
        form = NaviSectorForm(instance=sector)

    param["form"] = form
    param["SectorName"] = sector.name
    param["items"] = NavigatorItem.objects.filter(sector_id=secid)

    return render(request, "admin/admin_navi_item_index.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_item_create_view(request, secid):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    if request.method == "POST":
        form = NavigatorItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ADMNaviItemIndex", secid=secid)
    else:
        form = NavigatorItemForm
    param["form"] = form
    return render(request, "admin/admin_navi_item_create.html", param)


@csrf_exempt
def admin_article_image_upload(request):
    if request.method == "POST":
        upload_time = timezone.now()
        f = request.FILES["file"]

        file_name_suffix = f.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg"]:
            return JsonResponse({"message": file_upload_err_wrong_format})

        upload_path = os.path.join(
            MEDIA_ROOT,
            "article",
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file_path = os.path.join(upload_path, f.name)
        file_url = f'{MEDIA_URL}article/{upload_time.year}/{upload_time.month}/{upload_time.day}/{f.name}'
        if os.path.exists(file_path):
            return JsonResponse({
                "message": file_upload_err_already_exists,
                "location": file_url
            })

        with open(file_path, "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

        return JsonResponse({
            "location": file_url
        })
    else:
        return HttpResponse()
