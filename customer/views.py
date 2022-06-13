from datetime import datetime, timedelta, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_sameorigin

from customer.forms import ContactForm, CustomerLoginForm, CustomerRegisterForm, MeetingSlotFilter, AppointmentForm
from customer.models import Customer
from customer.utils import get_customer_info, get_news, get_index_list
from staring.customerSettings import Languages
from staring.models import Article, User, MeetingSlot, Appointment
from staring.text import UserNotExist_text


# Create your views here.
def index(request):
    param = {
        "page_title": _("星环首页"),
        "languages": Languages,
        "title_img": True,
        "ContactForm": True,
        "newsSectors": get_news(),
        "indexList": get_index_list(),
        **get_customer_info()
    }
    if request.user_agent.is_mobile:
        return render(request, "customer/tele/tele_index1.html", param)
    else:
        return render(request, "customer/index.html", param)


def customer_login_view(request):
    param = {
        "page_title": _("星环-登录"),
        "languages": Languages,
        "title_img": False,
        **get_customer_info(),
    }

    try:
        next_url = request.GET.get("next")
    except IndexError:
        next_url = ""

    if request.user.is_authenticated:
        return HttpResponseRedirect(next_url)

    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            paswd = form.cleaned_data.get("password")

            user = authenticate(
                request=request,
                username=username,
                password=paswd
            )
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _("登录成功"))
                if next_url:
                    return HttpResponseRedirect(next_url)
                return redirect("CUSTIndex")
            else:
                form.add_error(None, ValidationError(UserNotExist_text, code="UserNotExist"))

            param["form"] = form
            return render(request, "customer/login.html", param)

        else:
            param["form"] = form
            return render(request, "customer/login.html", param)
    else:
        param["form"] = CustomerLoginForm()
        return render(request, "customer/login.html", param)


def customer_logout(request):
    logout(request)
    return redirect('CUSTIndex')


def customer_register(request):
    param = {
        "page_title": _("星环-注册中心"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(),
    }

    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data["password1"]
            )
            u.name = form.cleaned_data["name"]
            u.countryCode = form.cleaned_data["countryCode"]
            u.tele = form.cleaned_data["tele"]
            u.save()

            c = Customer(user=u)
            c.save()

            login(request, user=u, backend='django.contrib.auth.backends.ModelBackend')

            messages.add_message(request, messages.SUCCESS, _("恭喜你注册成功"))
            return redirect("CUSTIndex")
        else:
            param["form"] = form
            return render(request, "customer/register.html", param)
    else:
        param["form"] = CustomerRegisterForm()
        return render(request, "customer/register.html", param)


@login_required(login_url="CUSTLogin")
def customer_center_view(request):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": User.objects.get(uid=request.user.uid),
        "title_img": True,
        # "profile": Customer.objects.get(user=request.user),
        **get_customer_info(),
    }

    return render(request, "customer/customer_center.html", param)


def customer_articles(request, article_id):
    param = {
        "page_title": _("星环"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(),
    }

    if request.method == "POST":
        contactForm = ContactForm(request.POST)
        if "contact" in request.POST:
            if contactForm.is_valid():
                contactForm.save()
                messages.add_message(request, messages.SUCCESS, _("提交成功"))
        param["ContactForm"] = ContactForm()
    else:
        param["ContactForm"] = ContactForm()

    article = get_object_or_404(Article, id=article_id, status="PUBLISH")
    article.view_count += 1
    article.save(update_fields=["view_count"])
    param["article"] = article

    if request.user_agent.is_mobile:
        return render(request, "customer/tele/customer_tele_articles.html", param)
    else:
        return render(request, "customer/customer_articles.html", param)


def customer_search_view(request, page):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": request.user,
        **get_customer_info(),
    }

    if request.GET.get("search"):
        q = request.GET.get("search")
        request.session["search"] = q
    elif request.session["search"] and not request.GET.get("search"):
        q = request.session["search"]
    else:
        q = ""

    param["search"] = q

    articles = Article.objects.filter(status="PUBLISH").filter(Q(title__icontains=q) | Q(content__icontains=q)) \
        .order_by("-last_update", "-view_count")

    p = Paginator(articles, 10)
    param["paginator"] = p
    param["results"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, 'customer/customer_search.html', param)


@login_required(login_url="CUSTLogin")
def customer_appointment_view (request):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": request.user,
        "title_img": True,
        **get_customer_info(),
    }

    start = datetime.today().date() + timedelta(days=1)
    end = datetime.today().date() + timedelta(days=14)
    initial = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    }

    if request.method == "POST":
        form = MeetingSlotFilter(request.POST, initial=initial)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            if start_date > datetime.today().date():
                start = start_date

            if end_date:
                end = end_date

        else:
            form = MeetingSlotFilter(request.POST, initial=initial)
    else:
        form = MeetingSlotFilter(initial=initial)

    slots = MeetingSlot.objects.filter(start_datetime__gte=start, end_datetime__lte=end, availability__gt=0)\
        .order_by("start_datetime")
    param["slots"] = slots
    param["form"] = form
    return render(request, "customer/customer_appointment.html", param)


@login_required(login_url="CUSTLogin")
def customer_appointment_2_view(request, slot_id):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": request.user,
        "title_img": True,
        **get_customer_info(),
    }

    slot = MeetingSlot.objects.get(id=slot_id)
    param["slot"] = slot

    if request.method == "POST":
        pass
    else:
        pass

    return render(request, "customer/customer_appointment_2.html", param)


@xframe_options_sameorigin
def customer_contact_form_frame(request):
    param = {
        "user": request.user,
        **get_customer_info(),
    }

    if request.method == "POST":
        contactForm = ContactForm(request.POST)
        if "contact" in request.POST:
            if contactForm.is_valid():
                contactForm.save()
        param["ContactForm"] = ContactForm()
    else:
        param["ContactForm"] = ContactForm()

    return render(request, 'customer/customer_contact.html', param)
