from django.contrib import admin
from django.db.models import QuerySet

from api.models import Thread, ThreadMessage, InitThread


@admin.action(description="Delete selected (No Confirmation)")
def delete_selected_no_conf(modeladmin, request, queryset):
    queryset.delete()


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    fields = (
        "thread_id",
        "time_opened",
        "opened_by",
        "generic_topic",
        "specific_topic",
        "time_closed",
        "closed_by",
    )
    list_display = (
        "thread_id",
        "time_opened",
        "opened_by",
        "generic_topic",
        "time_closed",
        "closed_by",
    )
    search_fields = (
        "thread_id",
        "time_opened",
        "opened_by",
        "generic_topic",
        "time_closed",
        "closed_by",
    )
    list_filter = ("generic_topic", "opened_by", "closed_by")
    actions = (delete_selected_no_conf,)
    date_hierarchy = "time_opened"


@admin.register(ThreadMessage)
class ThreadMessageAdmin(admin.ModelAdmin):
    def related_thread_id(self, obj):
        return obj.thread.thread_id

    list_display = ("related_thread_id", "author_id", "time_sent", "is_helper")
    search_fields = ("related_thread_id", "author_id", "time_sent", "is_helper")
    list_filter = (
        "is_helper",
        "author_id",
        ("thread", admin.RelatedOnlyFieldListFilter),
    )
    actions = (delete_selected_no_conf,)
    date_hierarchy = "time_sent"


@admin.register(InitThread)
class InitThreadAdmin(admin.ModelAdmin):
    list_display = ("thread_id", "help_type", "created_at")
    search_fields = ("thread_id", "help_type")
    actions = (delete_selected_no_conf,)
    date_hierarchy = "created_at"
