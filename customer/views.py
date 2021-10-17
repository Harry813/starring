from django.contrib.auth import authenticate, login, logout
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

    return render(request, "customer/index.html", param)


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
