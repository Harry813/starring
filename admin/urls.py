from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index_view, name='ADMIndex'),
    path('login/', views.admin_login_view, name='ADMLogin'),
    path('logout/', views.admin_logout_view, name='ADMLogout'),
    path('articles/page<int:page>/', views.admin_article_index_view, name="ADMArticleIndex"),
    path('articles/create/', views.admin_article_create_view, name="ADMArticleCreate"),
    path('articles/article-<int:article_id>/', views.admin_article_edit_view, name="ADMArticleEdit"),
    path('customer/page<int:page>/', views.admin_customer_index_view, name="ADMCustomerIndex"),
    path('customer/profile-<uuid:customer_id>/', views.admin_customer_edit_view, name="ADMCustomerEdit")
]
