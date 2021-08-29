from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index_view, name='ADMIndex'),
    path('login/', views.admin_login_view, name='ADMLogin'),
    path('template/', views.admin_article_create_view, name='ADMArticleCreate')
]