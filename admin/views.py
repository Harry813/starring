import os
from datetime import datetime, date, time, timedelta

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
from admin.forms import *
from admin.models import Staff
from admin.utils import get_admin_info, reorder
from customer.models import Customer, Consult
from staring.customerSettings import Languages
from staring.settings import MEDIA_ROOT, MEDIA_URL, DOMAIN_NAME
from staring.text import *
from staring.utils import get_basic_info


def admin_login_view (request):
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


def admin_logout_view (request):
    logout(request)
    return redirect("ADMLogin")


@login_required(login_url="ADMLogin")
def admin_index_view (request):
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
def admin_article_index_view (request, page):
    param = {
        "page_title": _("星环-文章管理"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        **get_basic_info(),
        **get_admin_info(),
    }

    articles = Article.admin_visible.all()

    if request.method == "POST":
        form = ArticleSearchForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            if status != "":
                if status == "DELETE":
                    articles = Article.objects.filter(status="DELETE")
                else:
                    articles = articles.filter(status=status)

            lv_require = form.cleaned_data.get("lv_require")
            if lv_require >= 0:
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
    param["paginator"] = p
    param["article_list"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    param["SearchForm"] = form

    return render(request, "admin/admin_article_index.html", param)


@login_required(login_url="ADMLogin")
def admin_article_create_view (request):
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
            form = ArticleForm(request.POST)
    else:
        form = ArticleForm()
    param["form"] = form
    return render(request, "admin/admin_article_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_article_edit_view (request, article_id):
    param = {
        "page_title": _("星环-文章编辑"),
        "languages": Languages,
        "active_page": "ADMArticleIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    article = get_object_or_404(Article, id=article_id)
    param["view_count"] = article.view_count

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            # Todo: add a permission check
            return redirect("ADMArticleIndex", 1)
        else:
            form = ArticleForm(request.POST, instance=article)
    else:
        form = ArticleForm(instance=article)

    param["form"] = form
    return render(request, "admin/admin_article_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_article_delete_view (request, article_id):
    article = Article.objects.get(id=article_id)
    if article.status != "DELETE":
        article.status = "DELETE"
        article.save()
    else:
        article.delete()
    return redirect("ADMArticleIndex", 1)


@login_required(login_url="ADMLogin")
def admin_customer_index_view (request, page=1):
    param = {
        "page_title": _("星环-用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    user_query = User.objects.filter(uid__in=Customer.objects.values_list("user_id", flat=True))

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
def admin_customer_edit_view (request, customer_id):
    param = {
        "page_title": _("星环-用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        "uid": customer_id,
        **get_basic_info(),
        **get_admin_info()
    }

    user = get_object_or_404(User, uid=customer_id)
    customer_profile = Customer.objects.get_or_create(user=user)[0]
    basic_initial = {"dob": user.format_dob}
    param["customer"] = customer_profile

    if request.method == "POST":
        basic_form = UserForm(request.POST, instance=user, initial=basic_initial)
        customer_form = CustomerForm(request.POST, instance=customer_profile)

        if basic_form.is_valid():
            basic_form.save()
        else:
            basic_form = UserForm(request.POST, instance=user, initial=basic_initial)

        if customer_form.is_valid():
            customer_form.save()
        else:
            customer_form = CustomerForm(request.POST, instance=customer_profile)
    else:
        basic_form = UserForm(instance=user, initial=basic_initial)
        customer_form = CustomerForm(instance=customer_profile)

    param["basic_form"] = basic_form
    param["customer_form"] = customer_form
    return render(request, "admin/admin_customer_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_crs_view (request, crs_id):
    param = {
        "page_title": _("星环-用户管理"),
        "languages": Languages,
        "active_page": "ADMCustomerIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    evaluation = get_object_or_404(CRS, id=crs_id)
    param["crs"] = evaluation
    param["user_id"] = evaluation.customer.user.uid
    return render(request, "admin/admin_customer_crs.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_index_view (request, page=1):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        **get_basic_info(),
        **get_admin_info()
    }

    user_query = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).exclude(username="AnonymousUser")

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
def admin_staff_edit_view (request, staff_id):
    param = {
        "page_title": _("星环-员工管理"),
        "languages": Languages,
        "active_page": "ADMStaff",
        "uid": staff_id,
        **get_basic_info(),
        **get_admin_info()
    }

    user_query = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).exclude(username="AnonymousUser")
    basic_profile = get_object_or_404(user_query, uid=staff_id)
    basic_initial = {"dob": basic_profile.format_dob}
    param["user_id"] = staff_id
    staff_profile = Staff.objects.get_or_create(user_id=staff_id, defaults={'user': basic_profile})[0]

    if request.method == "POST":
        basic_form = UserForm(request.POST, instance=basic_profile, initial=basic_initial, prefix="basic")
        staff_form = StaffForm(request.POST, instance=staff_profile, prefix="staff")

        if basic_form.is_valid():
            basic_form.save()
        else:
            basic_form = UserForm(request.POST, instance=basic_profile, initial=basic_initial, prefix="basic")

        if staff_form.is_valid():
            staff_form.save()
        else:
            staff_form = StaffForm(request.POST, instance=staff_profile, prefix="staff")

        if basic_form.is_valid() and staff_form.is_valid():
            pass
        else:
            pass

    else:
        basic_form = UserForm(instance=basic_profile, initial=basic_initial, prefix="basic")
        staff_form = StaffForm(instance=staff_profile, prefix="staff")

    param["basic_form"] = basic_form
    param["staff_form"] = staff_form
    return render(request, "admin/admin_staff_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_staff_create_view (request):
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
def admin_news_sector_index_view (request):
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
    return render(request, 'admin/admin_sector_index.html', param)


@login_required(login_url="ADMLogin")
def admin_news_sector_edit_view (request, sid):
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
    param["sector"] = sector
    param["news"] = News.objects.filter(sector=sector)
    return render(request, 'admin/admin_sector_edit.html', param)


@login_required(login_url="ADMLogin")
def admin_news_create_view (request, sid):
    param = {
        "page_title": _("星环-新闻创建"),
        "languages": Languages,
        "active_page": "ADMNewsSectorIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = NewsSector.objects.get(id=sid)
    initial = {"sector": sector, "order": len(News.objects.filter(sector=sector)) + 1}

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(News, Q(sector_id=sector), item, order)
            return redirect("ADMNewsSectorEdit", sid=sid)
        else:
            form = NewsForm(request.POST, request.FILES)
    else:
        form = NewsForm()

    param["form"] = form
    return render(request, "admin/admin_news_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_news_edit_view (request, sid, nid):
    param = {
        "page_title": _("星环-新闻编辑"),
        "languages": Languages,
        "active_page": "ADMNewsSectorIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = NewsSector.objects.get(id=sid)
    news = News.objects.get(id=nid)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news, initial={"reorder": news.order + 1})
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(News, Q(sector_id=sector), item, order)
            return redirect("ADMNewsSectorEdit", sid=sid)
        else:
            form = NewsForm(request.POST, request.FILES, instance=news, initial={"reorder": news.order + 1})
    else:
        form = NewsForm(instance=news, initial={"reorder": news.order + 1})

    param["form"] = form
    return render(request, "admin/admin_news_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_news_delete (request, sid, nid):
    News.objects.filter(sector_id=sid, id=nid).delete()
    reorder(News, Q(sector_id=sid))
    return redirect("ADMNewsSectorEdit", secid=sid)


@login_required(login_url="ADMLogin")
def admin_slot_index_view (request, page):
    param = {
        "page_title": _("星环-日程管理"),
        "languages": Languages,
        "active_page": "ADMSlotIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    timeslots = MeetingSlot.objects.filter(start_datetime__gte=datetime.today()).order_by("start_datetime")

    p = Paginator(timeslots, 10)
    timeslots = p.get_page(page)
    param["paginator"] = p
    param["timeslots"] = timeslots
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_slots.html", param)


@login_required(login_url="ADMLogin")
def admin_slot_create_view (request):
    param = {
        "page_title": _("星环-日程管理"),
        "languages": Languages,
        "active_page": "ADMSlotIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    if request.method == "POST":
        form = SlotGeneratorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ADMSlotIndex", page=1)
        else:
            form = SlotGeneratorForm(request.POST)
    else:
        form = SlotGeneratorForm()

    param["form"] = form
    return render(request, "admin/admin_slot_create.html", param)


@login_required(login_url="ADMLogin")
def admin_slot_edit_view (request, sid):
    param = {
        "page_title": _("星环-日程管理"),
        "languages": Languages,
        "active_page": "ADMSlotIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    slot = get_object_or_404(MeetingSlot, id=sid)
    param["slot"] = slot

    if request.method == "POST":
        form = SlotEditForm(request.POST, initial=slot.as_property)
        if form.is_valid():
            d = form.cleaned_data.get("date")
            start_time = form.cleaned_data.get("start_time")
            end_time = form.cleaned_data.get("end_time")
            start_datetime = datetime.combine(d, start_time)
            end_datetime = datetime.combine(d, end_time)

            slot.start_datetime = start_datetime
            slot.end_datetime = end_datetime
            slot.save()
            return redirect("ADMSlotIndex", page=1)
        else:
            form = SlotEditForm(request.POST, initial=slot.as_property)
    else:
        form = SlotEditForm(initial=slot.as_property)

    param["form"] = form
    return render(request, "admin/admin_slot_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_sector_index_view (request):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        "sectors": NavigatorSector.objects.all(),
        **get_basic_info(),
        **get_admin_info()
    }
    initial = {"order": len(NavigatorSector.objects.all()) + 1}

    if request.method == "POST":
        form = NaviSectorForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
        else:
            form = NaviSectorForm(request.POST, initial=initial)
    else:
        form = NaviSectorForm()

    param["form"] = form

    return render(request, "admin/admin_navi_sector_index.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_sector_delete (request, secid):
    try:
        NavigatorSector.objects.get(id=secid).delete()
    except ValidationError:
        pass
    return redirect("ADMNaviSectorIndex")


@login_required(login_url="ADMLogin")
def admin_navi_item_index_view (request, secid):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        "SectorId": secid,
        **get_basic_info(),
        **get_admin_info()
    }
    sector = NavigatorSector.objects.get(id=secid)

    if request.method == "POST":
        form = NaviSectorForm(request.POST, instance=sector)
        if form.is_valid():
            item = form.save(commit=False)
            reorder(NavigatorSector, item=item)
        else:
            form = NaviSectorForm(request.POST, instance=sector)
    else:
        form = NaviSectorForm(instance=sector)

    param["form"] = form
    param["SectorName"] = sector.name
    param["items"] = NavigatorItem.objects.filter(sector_id=secid)

    return render(request, "admin/admin_navi_item_index.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_item_create_view (request, secid):
    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = NavigatorSector.objects.get(id=secid)
    param["SectorName"] = sector.name
    initial = {"sector": sector, "reorder": len(NavigatorItem.objects.filter(sector=sector)) + 1}
    if request.method == "POST":
        form = NavigatorItemForm(request.POST, initial=initial)
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(NavigatorItem, Q(sector_id=sector), item, order)
            return redirect("ADMNaviItemIndex", secid=secid)
        else:
            form = NavigatorItemForm(request.POST, initial=initial)
    else:
        form = NavigatorItemForm(initial=initial)
    param["form"] = form
    return render(request, "admin/admin_navi_item_ce.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_item_edit_view (request, secid, itemid):
    sector = NavigatorSector.objects.get(id=secid)
    item = NavigatorItem.objects.get(id=itemid)

    param = {
        "page_title": _("星环-导航栏管理"),
        "languages": Languages,
        "active_page": "ADMNaviIndex",
        "SectorName": sector.name,
        **get_basic_info(),
        **get_admin_info()
    }
    if request.method == "POST":
        form = NavigatorItemForm(request.POST, instance=item, initial={"reorder": item.order + 1})
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(NavigatorItem, Q(sector_id=sector), item, order)
            return redirect("ADMNaviItemIndex", secid=secid)
        else:
            form = NavigatorItemForm(request.POST, instance=item, initial={"reorder": item.order + 1})
    else:
        form = NavigatorItemForm(instance=item, initial={"reorder": item.order + 1})
    param["form"] = form
    return render(request, "admin/admin_navi_item_ce.html", param)


@login_required(login_url="ADMLogin")
def admin_navi_item_delete (request, secid, itemid):
    NavigatorItem.objects.get(id=itemid).delete()
    reorder(NavigatorItem, Q(sector_id=secid))
    return redirect("ADMNaviItemIndex", secid=secid)


@login_required(login_url="ADMLogin")
def admin_index_sector_index (request):
    param = {
        "page_title": _("星环-首页清单管理"),
        "languages": Languages,
        "active_page": "ADMIndListIndex",
        "sectors": IndexListSector.objects.all(),
        "itemCount": IndexListItem.objects.count(),
        **get_basic_info(),
        **get_admin_info()
    }
    if request.method == "POST":
        form = IndexListSectorForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = IndexListSectorForm(request.POST)
    else:
        form = IndexListSectorForm()

    param["form"] = form

    return render(request, "admin/admin_indList_sector_index.html", param)


@login_required(login_url="ADMLogin")
def admin_index_sector_edit (request, secid):
    param = {
        "page_title": _("星环-首页清单管理"),
        "languages": Languages,
        "active_page": "ADMIndListIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = IndexListSector.objects.get(id=secid)

    if request.method == "POST":
        form = IndexListSectorForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
        else:
            form = IndexListSectorForm(request.POST, instance=sector)
    else:
        form = IndexListSectorForm(instance=sector)
    param["form"] = form
    param["items"] = IndexListItem.objects.filter(sector=sector)
    param["sector"] = sector

    return render(request, "admin/admin_indList_sector_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_index_item_create (request, secid):
    param = {
        "page_title": _("星环-首页清单管理"),
        "languages": Languages,
        "active_page": "ADMIndListIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    sector = IndexListSector.objects.get(id=secid)
    initial = {"sector": sector, "reorder": len(IndexListItem.objects.filter(sector=sector)) + 1}

    if request.method == "POST":
        form = IndexListItemForm(request.POST, initial=initial)
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(IndexListItem, Q(sector_id=sector), item, order)
            return redirect("ADMIndListSectorEdit", secid=secid)
        else:
            form = IndexListItemForm(request.POST, initial=initial)
    else:
        form = IndexListItemForm(initial=initial)

    param["form"] = form
    return render(request, "admin/admin_indList_item_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_index_item_edit (request, secid, itemid):
    param = {
        "page_title": _("星环-首页清单管理"),
        "languages": Languages,
        "active_page": "ADMIndListIndex",
        "sector": IndexListSector.objects.get(id=secid),
        **get_basic_info(),
        **get_admin_info()
    }
    sector = IndexListSector.objects.get(id=secid)
    item = IndexListItem.objects.get(id=itemid)
    if request.method == "POST":
        form = IndexListItemForm(request.POST, instance=item, initial={"reorder": item.order + 1})
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(IndexListItem, Q(sector_id=sector), item, order)
            return redirect("ADMIndListSectorEdit", secid=secid)
        else:
            form = IndexListItemForm(request.POST, instance=item, initial={"reorder": item.order + 1})
    else:
        form = IndexListItemForm(instance=item, initial={"reorder": item.order + 1})
    param["form"] = form
    return render(request, "admin/admin_indList_item_CE.html", param)


@login_required(login_url="ADMLogin")
def admin_index_item_delete (request, secid, itemid):
    IndexListItem.objects.get(id=itemid).delete()
    reorder(IndexListItem, Q(sector_id=secid))
    return redirect("ADMIndListSectorEdit", secid=secid)


@login_required(login_url="ADMLogin")
def admin_sidebar_index_view (request):
    param = {
        "page_title": _("星环-侧栏管理"),
        "languages": Languages,
        "active_page": "ADMSidebarIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    initial = {"reorder": len(IndexSidebarItem.objects.all()) + 1}
    if request.method == "POST":
        form = IndexSidebarForm(request.POST, initial=initial)
        if form.is_valid():
            item = form.save(commit=False)
            reorder(IndexSidebarItem, item=item)
        else:
            form = IndexSidebarForm(request.POST, initial=initial)
    else:
        form = IndexSidebarForm(initial=initial)
    param["form"] = form

    sidebar_items = IndexSidebarItem.objects.all()
    param["sidebar_items"] = sidebar_items
    param["count"] = len(sidebar_items)
    return render(request, "admin/admin_sidebar_index.html", param)


@login_required(login_url="ADMLogin")
def admin_sidebar_edit_view (request, sdb_id):
    param = {
        "page_title": _("星环-侧栏管理"),
        "languages": Languages,
        "active_page": "ADMSidebarIndex",
        **get_basic_info(),
        **get_admin_info()
    }

    item = IndexSidebarItem.objects.get(id=sdb_id)
    initial = {"reorder": item.order + 1}
    if request.method == "POST":
        form = IndexSidebarForm(request.POST, instance=item, initial=initial)
        if form.is_valid():
            item = form.save(commit=False)
            order = form.cleaned_data.get("reorder")
            reorder(IndexSidebarItem, q=Q(), item=item, index=order)
            return redirect("ADMSidebarIndex")
        else:
            form = IndexSidebarForm(request.POST, instance=item, initial=initial)
    else:
        form = IndexSidebarForm(instance=item, initial=initial)
    param["form"] = form
    return render(request, "admin/admin_sidebar_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_sidebar_delete_view (request, id):
    IndexSidebarItem.objects.get(id=id).delete()
    reorder(IndexSidebarItem)
    return redirect("ADMSidebarIndex")


@login_required(login_url="ADMLogin")
def admin_appointment_index_view (request, page):
    param = {
        "page_title": _("星环-预约管理"),
        "languages": Languages,
        "active_page": "ADMAppointmentIndex",
        **get_basic_info(),
        **get_admin_info(),
    }

    status_q = Q(status__in=["APPLY", "ACCEPT", "CASH", "PAID"])
    start_q = Q()
    end_q = Q()
    keyword_q = Q()

    if request.method == "POST":
        form = AppointmentFilterForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data["start_datetime"]
            if start_datetime:
                start_q = Q(slot__start_datetime__gte=start_datetime)

            end_datetime = form.cleaned_data["end_datetime"]
            if end_datetime:
                end_q = Q(slot__end_datetime__lte=end_datetime)

            status = form.cleaned_data["status"]
            if len(status) > 0:
                status_q = Q(status__in=status)

            keyword = form.cleaned_data["keyword"]
            if keyword:
                keyword_q = Q(id__icontains=keyword) | Q(name__icontains=keyword) | Q(email__icontains=keyword)

        else:
            form = AppointmentFilterForm(request.POST)
    else:
        form = AppointmentFilterForm()
    param["form"] = form

    appointments = Appointment.objects.filter(start_q & end_q & status_q & keyword_q)

    p = Paginator(appointments, 10)
    appointments = p.get_page(page)
    param["paginator"] = p
    param["appointments"] = appointments
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)

    return render(request, "admin/admin_appointment_index.html", param)


@login_required(login_url="ADMLogin")
def admin_appointment_edit_view (request, aptid):
    param = {
        "page_title": _("星环-预约管理"),
        "languages": Languages,
        "active_page": "ADMAppointmentIndex",
        **get_basic_info(),
        **get_admin_info(),
    }

    appointment = get_object_or_404(Appointment, id=aptid)
    param["appointment"] = appointment
    param["updates"] = MeetingUpdate.objects.filter(appointment=appointment).order_by('-last_update')
    old_status = appointment.get_status_display()

    if request.method == "POST":
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            new_app = form.save()
            new_status = new_app.get_status_display()
            if old_status != new_status:
                MeetingUpdate.objects.create(appointment=appointment, title=_("预约状态改变"),
                                             message=_("预约状态改变，由\"%(old_status)s\"改为\"%(new_status)s\"") % {
                                                 "old_status": old_status, "new_status": new_status
                                             })
        else:
            form = AppointmentStatusForm(request.POST, instance=appointment)
    else:
        form = AppointmentStatusForm(instance=appointment)
    param["form"] = form

    return render(request, "admin/admin_appointment_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_appointment_allocate_view (request, aptid=None):
    param = {
        "page_title": _("星环-预约管理"),
        "languages": Languages,
        "active_page": "ADMAppointmentIndex",
        **get_basic_info(),
        **get_admin_info(),
    }
    appointment = get_object_or_404(Appointment, id=aptid)
    param["appointment"] = appointment

    if request.method == "POST":
        form = AppointmentAllocateForm(request.POST, instance=appointment)
        staff_origin = appointment.staff

        if form.is_valid():
            form.save()
            staff_after = form.cleaned_data["staff"]

            if form.has_changed():
                if staff_origin is None:
                    MeetingUpdate.objects.create(appointment=appointment, title=_("咨询师添加"),
                                                 message=_("咨询师 %(staff_after)s 为您服务") % {
                                                     "staff_after": str(staff_after)
                                                 })
                elif staff_after is None:
                    MeetingUpdate.objects.create(appointment=appointment, title=_("咨询师取消"),
                                                 message=_("咨询师已被取消，请等待后续安排") % {
                                                     "staff_after": str(staff_after)
                                                 })
                else:
                    MeetingUpdate.objects.create(appointment=appointment, title=_("咨询师改变"),
                                                 message=_("咨询师由 %(staff_origin)s 改变为 %(staff_after)s") % {
                                                     "staff_after": str(staff_after), "staff_origin": str(staff_origin)
                                                 })

            return redirect("ADMAppointmentEdit", aptid=aptid)
        else:
            form = AppointmentAllocateForm(request.POST, instance=appointment)
    else:
        form = AppointmentAllocateForm(instance=appointment)

    param["form"] = form
    return render(request, "admin/admin_appointment_allocate.html", param)


@login_required(login_url="ADMLogin")
def admin_appointment_updates_view (request, aptid):
    param = {
        "page_title": _("星环-预约管理"),
        "languages": Languages,
        "active_page": "ADMAppointmentIndex",
        **get_basic_info(),
        **get_admin_info(),
    }
    appointment = get_object_or_404(Appointment, id=aptid)
    param["appointment"] = appointment
    param["updates"] = MeetingUpdate.objects.filter(appointment=appointment).order_by('-last_update')
    return render(request, "admin/admin_appointment_updates.html", param)


@login_required(login_url="ADMLogin")
def admin_appointment_update_create_view (request, aptid):
    param = {
        "page_title": _("星环-预约管理"),
        "languages": Languages,
        "active_page": "ADMAppointmentIndex",
        **get_basic_info(),
        **get_admin_info(),
    }

    appointment = get_object_or_404(Appointment, id=aptid)
    param["appointment"] = appointment
    initial = {"appointment": appointment}

    if request.method == "POST":
        form = MeetingUpdateForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            form.save()
            return redirect("ADMAppointmentEdit", aptid)
        else:
            form = MeetingUpdateForm(request.POST, request.FILES, initial=initial)
    else:
        form = MeetingUpdateForm(initial=initial)

    param["form"] = form
    return render(request, "admin/admin_meeting_update_create.html", param)


@login_required(login_url="ADMLogin")
def admin_appointment_accept (request, page, aptid):
    """Admin Convenience Function Accept"""
    appointment = Appointment.objects.get(id=aptid)
    appointment.status = "ACCEPT"
    appointment.save()
    MeetingUpdate.objects.create(appointment=appointment, title=_("预约已接受"),
                                 message=_("预约状态改变，预约被接受"))
    return redirect("ADMAppointmentIndex", page)


@login_required(login_url="ADMLogin")
def admin_appointment_reject (request, page, aptid):
    """Admin Convenience Function Reject"""
    appointment = Appointment.objects.get(id=aptid)
    appointment.status = "REJECT"
    appointment.save()
    MeetingUpdate.objects.create(appointment=appointment, title=_("预约已拒绝"),
                                 message=_("预约状态改变，预约被拒绝"))
    return redirect("ADMAppointmentIndex", page)


@login_required(login_url="ADMLogin")
def admin_appointment_success (request, page, aptid):
    """Admin Convenience Function Finish"""
    appointment = Appointment.objects.get(id=aptid)
    appointment.status = "SUCCESS"
    appointment.save()
    MeetingUpdate.objects.create(appointment=appointment, title=_("会议已完成"),
                                 message=_("预约状态改变，会议已完成"))
    return redirect("ADMAppointmentIndex", page)


@login_required(login_url="ADMLogin")
def admin_appointment_timeout (request, page, aptid):
    """Admin Convenience Function Timeout"""
    appointment = Appointment.objects.get(id=aptid)
    appointment.status = "TIMEOUT"
    appointment.save()
    MeetingUpdate.objects.create(appointment=appointment, title=_("会议超时未参加，请重新预约"),
                                 message=_("预约状态改变，会议超时未参加，请重新预约"))
    return redirect("ADMAppointmentIndex", page)


@login_required(login_url="ADMLogin")
def admin_appointment_paid (request, page, aptid):
    """Admin Convenience Function Paid"""
    appointment = Appointment.objects.get(id=aptid)
    appointment.status = "PAID"
    appointment.save()
    MeetingUpdate.objects.create(appointment=appointment, title=_("收费成功"),
                                 message=_("预约状态改变，收费成功"))
    return redirect("ADMAppointmentIndex", page)


@login_required(login_url="ADMLogin")
def admin_order_index_view (request, page):
    """Admin Convenience Function Order"""
    param = {
        "page_title": _("星环-订单管理"),
        "languages": Languages,
        "active_page": "ADMOrderIndex",
        **get_basic_info(),
        **get_admin_info(),
    }
    orders = Order.objects.order_by('-update_datetime')
    start_date_query = Q()
    end_date_query = Q()
    status_query = Q(status__in=["COMPLETED"])
    search_query = Q()
    if request.method == "POST":
        form = OrderSearchForm(request.POST)
        if form.is_valid():
            start_date_query = Q(create_datetime__gte=form.cleaned_data.get("start_date")) if form.cleaned_data.get(
                "start_date") else Q()
            end_date_query = Q(update_datetime__lte=form.cleaned_data.get("end_date")) if form.cleaned_data.get(
                "end_date") else Q()

            status_query = Q(status__in=form.cleaned_data.get("status")) if form.cleaned_data.get("status") else Q(
                status__in=["COMPLETED"])

            if form.cleaned_data.get("detail"):
                if form.cleaned_data.get("search_type") == "ID":
                    search_query = Q(id__contains=form.cleaned_data.get("detail")) | Q(
                        payment_id__contains=form.cleaned_data.get("detail"))
                elif form.cleaned_data.get("search_type") == "NAME":
                    search_query = Q(user__name__contains=form.cleaned_data.get("detail"))
        else:
            form = OrderSearchForm(request.POST)
    else:
        form = OrderSearchForm()

    orders = orders.filter(start_date_query & end_date_query & status_query & search_query)
    param["form"] = form
    p = Paginator(orders, 10)
    param["paginator"] = p
    param["orders"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_order_index.html", param)


@login_required(login_url="ADMLogin")
def admin_order_detail_view (request, order_id):
    """Admin Convenience Function Order Detail"""
    param = {
        "page_title": _("星环-订单管理"),
        "languages": Languages,
        "active_page": "ADMOrderIndex",
        **get_basic_info(),
        **get_admin_info(),
    }
    order = get_object_or_404(Order, id=order_id)
    param["order"] = order
    return render(request, "admin/admin_order_detail.html", param)


@login_required(login_url="ADMLogin")
def admin_consult_index_view(request, page):
    param = {
        "page_title": _("星环-咨询管理"),
        "languages": Languages,
        "active_page": "ADMConsultIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    consults = Consult.objects.all().order_by('-create_datetime')
    p = Paginator(consults, 10)
    param["paginator"] = p
    param["consults"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_consult_index.html", param)


@login_required(login_url="ADMLogin")
def admin_consult_detail_view(request, consult_id):
    param = {
        "page_title": _("星环-咨询管理"),
        "languages": Languages,
        "active_page": "ADMConsultIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    consult = get_object_or_404(Consult, id=consult_id)
    param["consult"] = consult

    if request.method == "POST":
        form = ConsultReplyForm(request.POST)
        if form.is_valid():
            form.send(consult.email)
            if consult.status == "O":
                consult.status = "T"
                consult.save()
            return redirect("ADMConsultDetail", consult_id)
        else:
            form = ConsultReplyForm(request.POST)
    else:
        form = ConsultReplyForm()
    param["form"] = form
    return render(request, "admin/admin_consult_detail.html", param)


@login_required(login_url="ADMLogin")
def admin_consult_close_util(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)
    consult.status = "C"
    consult.save()
    return redirect("ADMConsultDetail", consult_id)


@login_required(login_url="ADMLogin")
def admin_consult_trace_util(request, consult_id):
    consult = get_object_or_404(Consult, id=consult_id)
    consult.status = "T"
    consult.save()
    return redirect("ADMConsultDetail", consult_id)


@login_required(login_url="ADMLogin")
def admin_project_index_view(request, page):
    param = {
        "page_title": _("星环-移民项目管理"),
        "languages": Languages,
        "active_page": "ADMProjectIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    projects = Project.objects.all()
    p = Paginator(projects, 10)
    param["paginator"] = p
    param["projects"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_project_index.html", param)


@login_required(login_url="ADMLogin")
def admin_project_create_view (request):
    param = {
        "page_title": _("星环-移民项目管理"),
        "languages": Languages,
        "active_page": "ADMProjectIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    if request.method == "POST":
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ADMProjectIndex", 1)
        else:
            form = ProjectCreateForm(request.POST)
    else:
        form = ProjectCreateForm()

    param["form"] = form
    return render(request, "admin/admin_project_create.html", param)


@login_required(login_url="ADMLogin")
def admin_project_edit_view (request, project_id):
    param = {
        "page_title": _("星环-移民项目管理"),
        "languages": Languages,
        "active_page": "ADMProjectIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectEditForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("ADMProjectIndex", 1)
        else:
            form = ProjectEditForm(request.POST, instance=project)
    else:
        form = ProjectEditForm(instance=project)

    param["form"] = form
    return render(request, "admin/admin_project_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_case_index_view (request, page):
    param = {
        "page_title": _("星环-案例管理"),
        "languages": Languages,
        "active_page": "ADMCaseIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    cases = Case.objects.all()

    if request.method == "POST":
        form = CaseSearchForm(request.POST)
        if form.is_valid():
            search_query = Q()
            if form.cleaned_data["project"]:
                search_query &= Q(id__icontains=form.cleaned_data["title"]) |\
                                Q(name_icontains=form.cleaned_data["title"])
            if form.cleaned_data["status"]:
                search_query &= Q(status=form.cleaned_data["status"])
            cases = cases.filter(search_query)
        else:
            form = CaseSearchForm(request.POST)
    else:
        form = CaseSearchForm()

    param["form"] = form
    p = Paginator(cases, 10)
    param["paginator"] = p
    param["cases"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, "admin/admin_case_index.html", param)


@login_required(login_url="ADMLogin")
def admin_case_create_view (request):
    param = {
        "page_title": _("星环-案例管理"),
        "languages": Languages,
        "active_page": "ADMCaseIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    if request.method == "POST":
        form = CaseCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ADMCaseIndex", 1)
        else:
            form = CaseCreateForm(request.POST)
    else:
        form = CaseCreateForm()

    param["form"] = form
    return render(request, "admin/admin_case_create.html", param)


@login_required(login_url="ADMLogin")
def admin_case_edit_view (request, case_id):
    param = {
        "page_title": _("星环-案例管理"),
        "languages": Languages,
        "active_page": "ADMCaseIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    case = get_object_or_404(Case, id=case_id)
    if request.method == "POST":
        form = CaseEditForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect("ADMCaseIndex", 1)
        else:
            form = CaseEditForm(request.POST, instance=case)
    else:
        form = CaseEditForm(instance=case)

    param["form"] = form
    param["case"] = case
    param["updates"] = CaseUpdate.objects.filter(case=case)
    param["files"] = CaseFile.objects.filter(case=case)
    return render(request, "admin/admin_case_edit.html", param)


@login_required(login_url="ADMLogin")
def admin_case_create_update_view(request, case_id):
    param = {
        "page_title": _("星环-案例管理"),
        "languages": Languages,
        "active_page": "ADMCaseIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    case = get_object_or_404(Case, id=case_id)
    initial = {"case": case}
    if request.method == "POST":
        form = CaseUpdateForm(request.POST, initial=initial)
        if form.is_valid():
            form.save()
            return redirect("ADMCaseEdit", case.id)
        else:
            form = CaseUpdateForm(request.POST, initial=initial)
    else:
        form = CaseUpdateForm(initial=initial)
    param["form"] = form
    param["case"] = case
    return render(request, "admin/admin_case_update.html", param)


@login_required(login_url="ADMLogin")
def admin_case_file_view(request, case_id):
    param = {
        "page_title": _("星环-案例管理"),
        "languages": Languages,
        "active_page": "ADMCaseIndex",
        **get_basic_info(),
        **get_admin_info()
    }
    case = get_object_or_404(Case, id=case_id)
    initial = {"case": case}
    if request.method == "POST":
        form = CaseFileForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            return redirect("ADMCaseEdit", case.id)
        else:
            form = CaseFileForm(request.POST, request.FILES, initial=initial)
    else:
        form = CaseFileForm(initial=initial)

    param["form"] = form
    param["case"] = case
    param["files"] = CaseFile.objects.filter(case=case)
    return render(request, "admin/admin_case_file.html", param)


@login_required(login_url="ADMLogin")
def admin_case_file_receive(request, file_id):
    f = get_object_or_404(CaseFile, id=file_id)
    f.status = "RECEIVED"
    f.save()
    return redirect(f.file.url)


@csrf_exempt
def admin_article_image_upload (request):
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
