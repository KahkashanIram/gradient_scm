from django.utils.timezone import now, timedelta
from inventory.models import InventoryBatch

class InventoryExpiryService:
    """
    Handles expired & near-expiry inventory
    """

    @staticmethod
    def get_expired():
        today = now().date()
        return InventoryBatch.objects.filter(expiry_date__lt=today)

    @staticmethod
    def get_near_expiry(days=30):
        threshold = now().date() + timedelta(days=days)
        return InventoryBatch.objects.filter(
            expiry_date__gte=now().date(),
            expiry_date__lte=threshold
        )
