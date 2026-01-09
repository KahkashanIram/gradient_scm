from django.utils.deprecation import MiddlewareMixin
from admin.utils import log_admin_activity


class AdminActivityMiddleware(MiddlewareMixin):
    """
    Auto-logs admin & system-level actions.
    """

    ADMIN_PATH_PREFIXES = (
        "/admin/",
        "/api/admin/",
        "/api/system/",
    )

    # 🔕 Paths that should NEVER be logged
    EXCLUDED_PATHS = (
        "/api/system/health/",
    )

    def process_response(self, request, response):
        try:
            if self._should_log(request):
                log_admin_activity(
                    user=getattr(request, "user", None),
                    action=self._resolve_action(request, response),
                    module=self._resolve_module(request),
                    request=request,
                    metadata={
                        "method": request.method,
                        "path": request.path,
                        "status_code": response.status_code,
                    },
                )
        except Exception:
            # Never block the request lifecycle
            pass

        return response

    def _should_log(self, request):
        # ❌ Exclude noisy endpoints
        if request.path in self.EXCLUDED_PATHS:
            return False

        return (
            hasattr(request, "user")
            and request.path.startswith(self.ADMIN_PATH_PREFIXES)
        )

    def _resolve_module(self, request):
        if request.path.startswith("/api/system/"):
            return "SYSTEM"
        if request.path.startswith("/api/admin/"):
            return "ADMIN"
        return "DJANGO_ADMIN"

    def _resolve_action(self, request, response):
        return f"{request.method}_{response.status_code}"
