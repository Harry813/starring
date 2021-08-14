"""staring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from staring import settings

# urlpatterns = [
#     path('sitemap.xml', sitemap, name='sitemap-xml'),
# ]

urlpatterns = i18n_patterns(
    # path('admin/', admin.site.urls),
    path('', include("customer.urls")),
    path('admin/', include("admin.urls"))
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


