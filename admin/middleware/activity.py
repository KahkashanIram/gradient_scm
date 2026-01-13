from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser

from admin.models.activity_log import AdminActivityLog


class AdminActivityMiddleware(MiddlewareMixin):
    """
    Enterprise-grade admin activity logger.

    Logs ONLY state-changing admin actions:
    - POST / PUT / PATCH / DELETE
    - Authenticated users only
    - Never breaks admin (fail-safe)
    """

    MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

    def process_response(self, request, response):
        try:
            # Only admin panel
            if not request.path.startswith("/admin/"):
                return response

            # Ignore static & media
            if request.path.startswith("/admin/static/"):
                return response

            # Log ONLY mutating requests (prevents duplicate GET noise)
            if request.method not in self.MUTATING_METHODS:
                return response

            user = getattr(request, "user", None)

            # Authenticated users only
            if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
                return response

            # Ignore login/logout endpoints
            if request.path in ("/admin/login/", "/admin/logout/"):
                return response

            AdminActivityLog.objects.create(
                admin_user=user,
                action="ADMIN_ACTION",
                resource_type="ADMIN",
                resource_id=None,
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                metadata={
                    "query_params": dict(request.GET),
                },
            )

        except Exception:
            # 🔒 ABSOLUTE SAFETY: logging must NEVER break admin
            pass

        return response

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
