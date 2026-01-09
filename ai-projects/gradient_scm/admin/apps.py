from django.apps import AppConfig

class AdminCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "admin"              # filesystem path (keep)
    label = "admin_core"        # ✅ UNIQUE LABEL (THIS FIXES IT)
    verbose_name = "Admin Core"
