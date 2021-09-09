from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

# Create your views here.
from customer.forms import ContactForm
from customer.utils import get_customer_info
from staring.models import Article


def index(request):
    param = {
        "page_title": _("星环首页"),
        "title_img": True,
        **get_customer_info(),
    }
    if request.method == "POST":
        contactForm = ContactForm(request.POST)
        if "contact" in request.POST:
            if contactForm.is_valid():
                # contact form success
                pass
        param["ContactForm"] = ContactForm()
    else:
        param["ContactForm"] = ContactForm()

    return render(request, "customer/index.html", param)


def customer_articles(request, article_id):
    param = {
        "page_title": _("星环"),
        **get_customer_info(),
    }

    if request.method == "POST":
        contactForm = ContactForm(request.POST)
        if "contact" in request.POST:
            if contactForm.is_valid():
                # contact form success
                return HttpResponse("<h1>Success</h1>")
        param["ContactForm"] = ContactForm()
    else:
        param["ContactForm"] = ContactForm()

    article = get_object_or_404(Article, id=article_id)
    param["article"] = article
    return render(request, "customer/customer_articles.html", param)
