"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UserAdmin.settings")
django.setup()

import lists.views

urlpatterns = [
    # `(blah)` 這種寫法會match anything, 然後變成 a argument 一併傳到 view_list() 中
    # trailing `/` for queries, not for actions
    url(r'^(\d+)/$', view=lists.views.view_list, name="view_list"),
    url(r'^(\d+)/add_item$', view=lists.views.add_item, name="add_item"),

    # trailing `/` for queries, don't do it for actions
    url(r'^new$', view=lists.views.new_list, name="new_list"),
]
