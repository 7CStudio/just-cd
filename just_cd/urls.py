"""just_cd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from just_cd.deploy_app import views

urlpatterns = [
    url(r'^deploy/e88e26fd-e45f-4e9c-8fca-5d42327a33ac/$', views.deploy_view),
    url(r'^status/([0-9]+)/$', views.build_detail_view, name='details'),
    url(r'^status/$', views.build_list_view),
    url(r'^admin/', admin.site.urls),
]
