from django.contrib import admin
from django.urls import path, include

admin.site.site_title = "Nextcord Statistics"  # The stuff shown in tabs
admin.site.site_header = "Nextcord Statistics Admin Page"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("", include("base.urls")),
]
