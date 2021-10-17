from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='CUSTIndex'),
    path('article/<int:article_id>/', views.customer_articles, name="article"),
    path('login/', views.customer_login, name="CUSTLogin"),
    path('logout/', views.customer_logout, name="CUSTLogout"),
    path('register/', views.customer_register, name="CUSTRegister"),
    path('profile/', views.customer_center_view, name="CUSTCenter"),
    path('search/<int:page>/', views.customer_search_view, name="CUSTSearch"),
    path('contact_form/', views.customer_contact_form_frame, name="CUSTContact")
]
