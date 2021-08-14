from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('updates/', views.updates, name='CUpdates')
]
