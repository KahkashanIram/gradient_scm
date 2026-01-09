from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils.timezone import now

from system.services.health_service import SystemHealthService


class SystemHealthAPIView(APIView):
    """
    Read-only system health endpoint.
    Admin-only.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        service = SystemHealthService()
        components = service.overall_status()

        overall_status = self._calculate_overall_status(components)

        return Response({
            "status": overall_status,
            "timestamp": now(),
            "components": components,
        })

    def _calculate_overall_status(self, components: dict) -> str:
        """
        Determine overall system health based on components.
        """
        statuses = [
            component.get("status")
            for component in components.values()
        ]

        if "down" in statuses:
            return "down"

        if "error" in statuses:
            return "degraded"

        if all(status == "ok" for status in statuses):
            return "ok"

        return "unknown"
