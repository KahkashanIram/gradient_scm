from django.contrib import admin
from admin.models import AdminActivityLog


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "admin_user",
        "module",
        "action",
        "ip_address",
    )

    list_filter = ("module", "action", "created_at")
    search_fields = ("admin_user__username", "action", "object_id")
    readonly_fields = [field.name for field in AdminActivityLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
