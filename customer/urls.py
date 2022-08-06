from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='CUSTIndex'),
    path('article/<int:article_id>/', views.customer_articles, name="article"),
    re_path(r'^login/$', views.customer_login_view, name="CUSTLogin"),
    path('logout/', views.customer_logout, name="CUSTLogout"),
    path('register/', views.customer_register, name="CUSTRegister"),
    path('profile/', views.customer_center_view, name="CUSTCenter"),
    path('appointment/', views.customer_appointment_view, name="CUSTAppoint"),
    path('appointment/<str:slot_id>/', views.customer_appointment_2_view, name="CUSTAppoint2"),
    path('appointment/payment/<str:appointment_id>/', views.customer_appointment_payment_view, name="CUSTAppointPay"),
    path('search/<int:page>/', views.customer_search_view, name="CUSTSearch"),
    path('contact_form/', views.customer_contact_form_frame, name="CUSTContact"),
    path('crs/', views.customer_self_assessment_crs_view, name="CUSTCRS"),
    path('crs/<str:crs_id>/', views.customer_crs_result_view, name="CUSTCRSResult"),
]
