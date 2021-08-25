from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from staring.customerSettings import Languages

# Create your views here.


def index(request):
    param = {
        "page_title": _("test")
    }
    return render(request, "admin/admin_login.html", param)


def admin_article_create_view(request):
    param = {
        "page_title": _("编辑"),
        "languages": Languages
    }
    return render(request, "admin/admin_template.html", param)
