from django.urls import path
from system.api.health import SystemHealthAPIView

urlpatterns = [
    path("health/", SystemHealthAPIView.as_view(), name="system-health"),
]
