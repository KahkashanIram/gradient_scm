from rest_framework import serializers
from admin.models.activity_log import AdminActivityLog


class AdminActivityLogSerializer(serializers.ModelSerializer):
    admin_user = serializers.SerializerMethodField()

    class Meta:
        model = AdminActivityLog
        fields = [
            "id",
            "created_at",
            "admin_user",
            "action",
            "resource_type",
            "method",
            "status_code",
        ]
        read_only_fields = fields

    def get_admin_user(self, obj):
        return obj.admin_user.username if obj.admin_user else None
