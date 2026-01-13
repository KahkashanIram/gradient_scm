from inventory.models import InventoryTransaction

class InventoryMovementService:
    """
    Full inventory audit trail
    """

    @staticmethod
    def get_history(item=None, batch=None):
        qs = InventoryTransaction.objects.select_related(
            "item", "batch"
        ).order_by("-created_at")

        if item:
            qs = qs.filter(item=item)

        if batch:
            qs = qs.filter(batch=batch)

        return qs
