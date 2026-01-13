from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from admin.models.activity_log import AdminActivityLog
from admin.api.serializers import AdminActivityLogSerializer


class AdminActivityLogListAPIView(ListAPIView):
    """
    Read-only API for admin audit logs.
    """
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return (
            AdminActivityLog.objects
            .select_related("admin_user")
            .order_by("-created_at")
        )
