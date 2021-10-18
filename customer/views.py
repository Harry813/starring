from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin

from customer.forms import ContactForm, CustomerLoginForm
from customer.models import Customer
from customer.utils import get_customer_info
from staring.customerSettings import Languages, IndexCarousel
from staring.models import Article, CarouselArticles, User
from staring.text import UserNoPermit_text, UserNotExist_text


# Create your views here.
def index(request):
    param = {
        "page_title": _("星环首页"),
        "languages": Languages,
        "title_img": True,
        "ContactForm": True,
        **get_customer_info(),
    }

    accordion = {}
    for key, title in IndexCarousel:
        accordion[title] = CarouselArticles.objects.filter(carousel=key)

    param["accordion"] = accordion

    return render(request, "customer/index.html", param)


def customer_login_view(request):
    param = {
        "page_title": _("星环-登录"),
        "languages": Languages,
        **get_customer_info(),
    }

    try:
        next_url = request.POST.get("next")
    except IndexError:
        next_url = ""

    if next_url == "None":
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
                else:
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


def customer_articles(request, article_id):
    param = {
        "page_title": _("星环"),
        "languages": Languages,
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

    article = get_object_or_404(Article, id=article_id)
    param["article"] = article
    return render(request, "customer/customer_articles.html", param)


def customer_logout(request):
    logout(request)
    return redirect('CUSTIndex')


def customer_register(request):
    param = {
        "page_title": _("星环-注册中心"),
        "languages": Languages,
        **get_customer_info(),
    }

    return render(request, "customer/register.html", param)


@login_required(login_url="CUSTLogin")
def customer_center_view(request):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": request.user,
        # "profile": Customer.objects.get(user=request.user),
        **get_customer_info(),
    }

    return render(request, "customer/customer_center.html", param)


def customer_search_view(request, page=1):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "user": request.user,
        **get_customer_info(),
    }

    q = request.GET.get("search")
    param["search"] = q

    articles = Article.objects.filter(status="PUBLISH").filter(Q(title__icontains=q) | Q(content__icontains=q))
    p = Paginator(articles, 30)

    param["paginator"] = p
    param["results"] = p.get_page(page)
    param["current_page"] = page
    param["page_list"] = p.get_elided_page_range(on_each_side=2, on_ends=2)
    return render(request, 'customer/customer_search.html', param)


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
