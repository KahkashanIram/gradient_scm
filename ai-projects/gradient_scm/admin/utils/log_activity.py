from typing import Optional, Dict
from django.http import HttpRequest
from admin.models import AdminActivityLog


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Extract client IP address safely.
    Handles reverse proxy headers if present.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_admin_activity(
    *,
    user,
    action: str,
    module: str,
    request: Optional[HttpRequest] = None,
    object_id: Optional[str] = None,
    metadata: Optional[Dict] = None,
):
    """
    Central admin/system activity logger.

    Parameters:
    - user: Django user instance (can be None for system actions)
    - action: What happened (LOGIN, CREATE_USER, FORCE_RELEASE_STOCK)
    - module: Where it happened (USERS, INVENTORY, SECURITY, SYSTEM)
    - request: HttpRequest (optional but recommended)
    - object_id: Affected object identifier
    - metadata: Extra structured context
    """

    try:
        AdminActivityLog.objects.create(
            admin_user=user if getattr(user, "is_authenticated", False) else None,
            action=action,
            module=module,
            object_id=str(object_id) if object_id else None,
            ip_address=get_client_ip(request) if request else None,
            user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
            metadata=metadata or {},
        )
    except Exception:
        # ❗ Never break the main flow due to logging failure
        # Logging must be NON-BLOCKING
        pass
