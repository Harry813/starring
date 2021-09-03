from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

# Create your views here.
from customer.utils import get_customer_info


def index(request):
    param = {
        "page_title": _("星环首页"),
        **get_customer_info(),
    }
    return render(request, "customer/index.html", param)


def updates(request):
    param = {
        "page_title": "更新记录"
    }
    param.update(getPanelInfo())
    return render(request, "Updates.html", param)
