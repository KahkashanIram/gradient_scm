from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AdminActivityLog(models.Model):
    """
    System-level admin activity log.
    Tracks WHO did WHAT, WHEN, and FROM WHERE.
    """

    admin_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_activity_logs",
    )

    action = models.CharField(
        max_length=100,
        help_text="Action performed (CREATE_USER, UPDATE_ROLE, LOGIN, etc.)"
    )

    module = models.CharField(
        max_length=50,
        help_text="System module (USERS, INVENTORY, SECURITY, SYSTEM)"
    )

    object_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Affected object identifier (if any)"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional contextual data"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "admin_activity_log"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["module"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.module} | {self.action} | {self.created_at}"
