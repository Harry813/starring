from django.shortcuts import render

# Create your views here.
from .api import *


def index(request):
    param = {
        "page_title": "test",
        "indexList": IndexListItems
    }
    param.update(getPanelInfo())
    return render(request, "customer/index.html", param)


def updates(request):
    param = {
        "page_title": "更新记录"
    }
    param.update(getPanelInfo())
    return render(request, "Updates.html", param)
