from django.contrib import admin
from django.urls import path, include   # ✅ include MUST be imported

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/system/", include("system.api.urls")),

    # Inventory APIs
    path("api/", include("inventory.api.urls")),

    # ✅ REQUIRED for Admin-logs
    path("api/admin/", include("admin.api.urls")),
]
