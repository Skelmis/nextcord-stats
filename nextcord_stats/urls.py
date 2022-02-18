from django.contrib import admin
from django.urls import path

admin.site.site_title = "Nextcord Statistics"
admin.site.site_header = "Nextcord Statistics"

urlpatterns = [
    path("admin/", admin.site.urls),
]
