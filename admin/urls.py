from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ADMLogin'),
    path('template/', views.admin_article_create_view, name='ADMArticleCreate')
]