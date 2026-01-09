from rest_framework import serializers
from admin.models import AdminActivityLog


class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin_user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = AdminActivityLog
        fields = [
            "id",
            "admin_user",
            "action",
            "module",
            "object_id",
            "ip_address",
            "created_at",
            "metadata",
        ]
        read_only_fields = fields
