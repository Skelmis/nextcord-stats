from django.urls import path

from base.views import sitemap_view

urlpatterns = [path("", sitemap_view, name="base-sitemap")]
