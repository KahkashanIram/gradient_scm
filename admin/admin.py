from django.contrib import admin
from django.utils import timezone
from admin.models import AdminActivityLog


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "admin_user",
        "action",
        "resource_type",
        "method",
        "status_code",
        "created_at",
    )
    def local_created_at(self, obj):
        return timezone.localtime(obj.created_at)

    local_created_at.short_description = "Time (Local)"

    list_filter = (
        "resource_type",
        "action",
        "method",
        "status_code",
        "created_at",
    )

    search_fields = (
        "admin_user__username",
        "resource_type",
        "resource_id",
        "path",
        "ip_address",
    )

    readonly_fields = (
        "admin_user",
        "action",
        "resource_type",
        "resource_id",
        "method",
        "path",
        "status_code",
        "ip_address",
        "user_agent",
        "metadata",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False