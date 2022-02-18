from django.contrib import admin
from django.urls import path, include

admin.site.site_title = "Nextcord Statistics"
admin.site.site_header = "Nextcord Statistics"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
]
