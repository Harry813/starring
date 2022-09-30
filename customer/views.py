import json
import urllib.parse
from datetime import datetime, timedelta
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersGetRequest

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_sameorigin

from customer.forms import ContactForm, CustomerLoginForm, CustomerRegisterForm, MeetingSlotFilter, AppointmentForm, \
    CRSForm
from customer.models import Customer
from customer.utils import get_customer_info, get_news, get_index_list
from staring.customerSettings import Languages
from staring.models import Article, User, MeetingSlot, Appointment, MeetingUpdate, CRS, Case, Subscription
from staring.models import Order as staringOrder
from staring.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_SECRET
from staring.text import UserNotExist_text
from staring.utils import generate_order_id, get_appt_price_total, send_email_with_template

if PAYPAL_MODE == "live":
    environment = LiveEnvironment(client_id=PAYPAL_CLIENT_ID, client_secret=PAYPAL_SECRET)
else:
    environment = SandboxEnvironment(client_id=PAYPAL_CLIENT_ID, client_secret=PAYPAL_SECRET)
client = PayPalHttpClient(environment)


# Create your views here.
def index (request):
    param = {
        "page_title": _("星环首页"),
        "languages": Languages,
        "title_img": True,
        "ContactForm": True,
        "newsSectors": get_news(),
        "indexList": get_index_list(),
        **get_customer_info(request)
    }
    # if request.user_agent.is_mobile:
    #     # return render(request, "customer/tele/tele_index1.html", param)
    #     return render(request, "customer/tele/tele_index.html", param)
    # else:
    return render(request, "customer/index.html", param)


def customer_login_view (request):
    param = {
        "page_title": _("星环-登录"),
        "languages": Languages,
        "title_img": False,
        **get_customer_info(request),
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
        else:
            form = CustomerLoginForm(request.POST)
    else:
        form = CustomerLoginForm()
    param["form"] = form
    return render(request, "customer/login.html", param)


def customer_logout (request):
    logout(request)
    return redirect('CUSTIndex')


def customer_register (request):
    param = {
        "page_title": _("星环-注册中心"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(request),
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

            context = {
                "title": _("注册成功"),
                "content": _(
                    "<p>您好，您已经成功注册星环账号，请妥善保管您的账号和密码。</p>"
                    "<p style='text-align: center'>账号：<strong>{}</strong></p>"
                    "<p style='text-align: center'>密码：<strong>{}</strong></p>"
                ).format(
                    form.cleaned_data['username'],
                    form.cleaned_data["password1"]
                )
            }

            if form.cleaned_data["subscribe"]:
                context["content"] += _("<p>您已经成功订阅了星环的最新资讯，我们会定期向您发送最新的资讯。</p>")
                Subscription.objects.create(
                    email=u.email,
                    tags = ["*"]
                )
            send_email_with_template(
                subject=_("星环-注册成功"),
                context=context,
                recipient_list=[u.email]
            )

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
def customer_center_view (request):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "title_img": True,
        # "profile": Customer.objects.get(user=request.user),
        **get_customer_info(request),
    }

    customer_profile = Customer.objects.get(user=request.user)
    appointments = Appointment.objects.filter(customer=customer_profile).order_by()
    param["appointments"] = appointments

    return render(request, "customer/customer_center.html", param)


def customer_articles (request, article_id):
    param = {
        "page_title": _("星环"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(request),
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


def customer_search_view (request, page):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        **get_customer_info(request),
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
        "title_img": True,
        **get_customer_info(request),
    }

    # user = User.objects.get(uid=request.user.uid)
    customer_profile = Customer.objects.get(user=request.user)
    q = Q(customer=customer_profile)

    # todo: 添加跳转
    if Appointment.objects.filter(q & Q(status__in=["APPLY", "UNPAID", "PAID", "ACCEPT", "CASH"])):
        pass

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

    slots = MeetingSlot.objects.filter(start_datetime__gte=start, end_datetime__lte=end, status="AVAILABLE") \
        .order_by("start_datetime")
    param["slots"] = slots
    param["form"] = form
    return render(request, "customer/customer_appointment.html", param)


@login_required(login_url="CUSTLogin")
def customer_appointment_2_view (request, slot_id):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(request),
    }

    slot = MeetingSlot.objects.get(id=slot_id)
    param["slot"] = slot
    u = User.objects.get(uid=request.user.uid)
    initial = {}
    if u.email:
        initial["email"] = u.email

    if u.name:
        initial["name"] = u.name

    if request.method == "POST":
        form = AppointmentForm(request.POST, initial=initial)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = "UNPAID"
            appointment.slot = slot
            appointment.customer = Customer.objects.get(user=u)
            appointment.save()
            slot.status = "LOCK"
            slot.save()
            return redirect("CUSTAppointPay", appointment_id=appointment.id)
        else:
            form = AppointmentForm(request.POST, initial=initial)
    else:
        form = AppointmentForm(initial=initial)

    param["form"] = form
    return render(request, "customer/customer_appointment_2.html", param)


@login_required(login_url="CUSTLogin")
def customer_appointment_payment_view (request, appointment_id):
    param = {
        "page_title": _("星环-我的主页"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(request),
    }
    appointment = get_object_or_404(Appointment, id=appointment_id)
    param["appointment"] = appointment

    slot = appointment.slot
    param["slot"] = slot
    param["subtotal"] = "{:.2f}".format(appointment.price)
    total = "{:.2f}".format(get_appt_price_total(appointment))
    param["total"] = total
    request.session["price"] = total

    return render(request, "customer/customer_appointment_payment.html", param)


def customer_self_assessment_crs_view (request):
    param = {
        "page_title": _("星环-CRS自我评估"),
        "languages": Languages,
        "title_img": True,
        **get_customer_info(request),
    }

    if request.method == "POST":
        form = CRSForm(request.POST)
        if form.is_valid():
            inst = form.save(commit=False)
            if request.user.is_authenticated:
                inst.customer = Customer.objects.get(user_id=request.user.uid)
            inst.save()
            return redirect("CUSTCRSResult", crs_id=inst.pk)
        else:
            form = CRSForm(request.POST)
    else:
        form = CRSForm()

    param["form"] = form

    return render(request, "customer/customer_self_assessment_crs_view.html", param)


def customer_crs_result_view (request, crs_id):
    param = {
        "page_title": _("星环-CRS评估报告"),
        "languages": Languages,
        **get_customer_info(request),
    }

    crs = get_object_or_404(CRS, id=crs_id)
    param["crs"] = crs
    if crs.customer is None and request.user.is_authenticated:
        crs.customer = Customer.objects.get(user_id=request.user.uid)
        crs.save()
    return render(request, "customer/customer_crs_report.html", param)


@login_required(login_url="CUSTLogin")
def create_appt_order (request, appointment_id):
    vip_lv = Customer.objects.get(user=User.objects.get(uid=request.user.uid)).vip_lv
    order_type = f"0{vip_lv}"

    appointment = Appointment.objects.get(id=appointment_id)
    price = request.session.pop("price")

    order_id = generate_order_id()
    order_request = OrdersCreateRequest()
    order_request.prefer('return=representation')
    order_request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "reference_id": order_id,
            "amount": {
                "currency_code": "CAD",
                "value": str(price)
            }
        }]
    })

    response = client.execute(order_request)
    result = response.result
    staringOrder.objects.create(
        id=order_id,
        payment_id=result.id,
        product_id=appointment_id,
        order_type=order_type,
        price=appointment.price,
    )
    return JsonResponse(data=result.dict(), safe=True)


@login_required(login_url="CUSTLogin")
def complete_appt_order (request, order_id):
    getRequest = OrdersGetRequest(order_id)
    response = client.execute(getRequest)
    result = response.result

    o = staringOrder.objects.get(payment_id=order_id)
    o.raw_json = json.dumps(result.dict())
    o.status = result.status
    o.save()

    appointment = Appointment.objects.get(id=o.product_id)
    appointment.status = "ACCEPT"
    appointment.save()

    slot = appointment.slot
    slot.status = "OCCUPIED"
    slot.save()
    return JsonResponse(data=result.dict(), safe=True)


@login_required(login_url="CUSTLogin")
def cash_payment_appt (request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.status = "CASH"
    appointment.save()

    slot = appointment.slot
    slot.status = "OCCUPIED"
    slot.save()
    return redirect("APPTPaymentSuccess", appointment_id=appointment_id)


@login_required(login_url="CUSTLogin")
def payment_success_view (request, appointment_id):
    param = {
        "page_title": _("星环-支付成功"),
        "languages": Languages,
        "appointment": Appointment.objects.get(id=appointment_id),
        **get_customer_info(request),
    }
    order = get_object_or_404(staringOrder, product_id=appointment_id)
    param["order"] = order
    return render(request, "customer/payment_success.html", param)


@login_required(login_url="CUSTLogin")
def subscribe_email (request):
    email = request.GET["subscribe_email"]
    if Subscription.objects.filter(email=email):
        return JsonResponse({"err": "Instance Already Exist"}, status=500)
    try:
        sub = Subscription.objects.create(email=email, tags=["*"])
        send_email_with_template(
            subject=_("星环-订阅成功"),
            context={
                "title": _("订阅成功"),
                "content": _("<p>您已经成功订阅了星环的最新资讯，我们会定期向您发送最新的资讯。</p>")
            },
            recipient_list=[email]
        )
        return JsonResponse({"subscription": sub.id}, status=200)
    except Exception:
        return JsonResponse({"err": "Unknown error"}, status=500)


def unsubscribe_email_view (request):
    param = {
        "page_title": _("星环-退订"),
        "languages": Languages,
        "email": request.user.email,
        **get_customer_info(request),
    }
    return render(request, "customer/unsubscribe.html", param)


def unsubscribe_email (request):
    email = request.GET["email"]
    try:
        Subscription.objects.get(email=email).delete()
        return JsonResponse({"email": email}, status=200)
    except Exception as e:
        return JsonResponse({"err": str(e)}, status=500)


@xframe_options_sameorigin
def customer_contact_form_frame (request):
    param = {
        **get_customer_info(request),
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
