from django.contrib import admin

from api.models import Thread, ThreadMessage


@admin.action(description="Delete selected (No Confirmation)")
def delete_selected_no_conf(modeladmin, request, queryset):
    queryset.delete()


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "thread_id",
        "time_opened",
        "opened_by",
        "topic",
        "time_closed",
        "closed_by",
    )
    search_fields = (
        "thread_id",
        "time_opened",
        "opened_by",
        "topic",
        "time_closed",
        "closed_by",
    )
    list_filter = ("topic", "opened_by", "closed_by")
    actions = (delete_selected_no_conf,)
    date_hierarchy = "time_opened"
    readonly_fields = ("thread_id", "time_opened")


@admin.register(ThreadMessage)
class ThreadMessageAdmin(admin.ModelAdmin):
    list_display = ("thread__thread_id", "author_id", "time_sent", "is_helper")
    search_fields = ("thread__thread_id", "author_id", "time_sent", "is_helper")
    list_filter = ("is_helper", "author_id", "thread__thread_id")
    actions = (delete_selected_no_conf,)
    date_hierarchy = "time_sent"
