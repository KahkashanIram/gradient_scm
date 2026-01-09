# admin/api/urls.py

from django.urls import path
from admin.api.activity_logs import AdminActivityLogListAPIView

urlpatterns = [
    path(
        "activity-logs/",
        AdminActivityLogListAPIView.as_view(),
        name="admin-activity-logs",
    ),
]
