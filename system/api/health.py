# system/api/health.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from system.api.authentication import CsrfExemptSessionAuthentication

from django.db import connections
import psutil
import platform
import time


class SystemHealthAPIView(APIView):
    """
    Admin-only system health endpoint
    - Session based
    - CSRF exempt (via custom authentication)
    """

    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Database check
        db_status = "ok"
        try:
            connections["default"].cursor()
        except Exception:
            db_status = "error"

        return Response({
            "timestamp": int(time.time()),
            "components": {
                "application": {
                    "status": "ok",
                    "details": {
                        "service": "Gradient SCM Backend",
                        "framework": "Django",
                    },
                },
                "database": {
                    "status": db_status,
                    "details": {
                        "engine": "PostgreSQL",
                    },
                },
                "system": {
                    "status": "ok",
                    "details": {
                        "cpu_percent": psutil.cpu_percent(interval=0.1),
                        "memory_percent": psutil.virtual_memory().percent,
                        "memory_total_mb": psutil.virtual_memory().total / 1024 / 1024,
                        "memory_available_mb": psutil.virtual_memory().available / 1024 / 1024,
                        "disk_percent": psutil.disk_usage("/").percent,
                        "disk_total_gb": psutil.disk_usage("/").total / 1024 / 1024 / 1024,
                        "disk_free_gb": psutil.disk_usage("/").free / 1024 / 1024 / 1024,
                        "platform": platform.system(),
                    },
                },
            },
        })
