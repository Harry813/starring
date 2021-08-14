from django.shortcuts import render

# Create your views here.


def index(request):
    param = {
        "page_title": "test"
    }
    return render(request, "customer/customer_template_basic.html", param)
