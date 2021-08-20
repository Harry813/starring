from django.shortcuts import render

# Create your views here.


def index(request):
    param = {
        "page_title": "test"
    }
    return render(request, "admin/admin_login.html", param)
