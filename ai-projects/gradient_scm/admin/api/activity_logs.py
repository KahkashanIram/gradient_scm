from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from admin.models import AdminActivityLog
from admin.api.serializers import AdminActivityLogSerializer


class AdminActivityLogListAPIView(ListAPIView):
    queryset = (
        AdminActivityLog.objects
        .select_related("user")
        .order_by("-created_at")
    )
    serializer_class = AdminActivityLogSerializer
    permission_classes = [IsAdminUser]
