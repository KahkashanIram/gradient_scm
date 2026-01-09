import psutil
import os


class SystemHealthService:
    """
    Collects system and dependency health information.
    """

    def check_application(self) -> dict:
        """
        Application-level health.
        If this code executes, Django is running.
        """
        return {
        "status": "ok",
        "details": {
            "service": "running",
        },
    }

    def check_database(self) -> dict:
        from django.db import connection, OperationalError

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")

            return {
                "status": "ok",
                "details": {
                    "engine": connection.vendor,
                },
            }

        except OperationalError as exc:
            return {
                "status": "down",
                "details": {"error": str(exc)},
            }

        except Exception as exc:
            return {
                "status": "error",
                "details": {"error": str(exc)},
            }

    def check_system_resources(self) -> dict:
        """
        Read-only system resource metrics:
        CPU, memory, disk usage.
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()

            # Root filesystem disk usage
            disk = psutil.disk_usage(os.sep)

            return {
                "status": "ok",
                "details": {
                    # CPU
                    "cpu_percent": cpu_percent,

                    # Memory
                    "memory_percent": memory.percent,
                    "memory_total_mb": round(memory.total / (1024 * 1024), 2),
                    "memory_available_mb": round(memory.available / (1024 * 1024), 2),

                    # Disk
                    "disk_percent": disk.percent,
                    "disk_total_gb": round(disk.total / (1024 ** 3), 2),
                    "disk_free_gb": round(disk.free / (1024 ** 3), 2),
                },
            }

        except Exception as exc:
            return {
                "status": "error",
                "details": {"error": str(exc)},
            }

    def overall_status(self) -> dict:
        return {
            "application": self.check_application(),
            "database": self.check_database(),
            "system": self.check_system_resources(),
        }
