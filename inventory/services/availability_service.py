from inventory.models import InventoryBatch


class InventoryAvailabilityService:
    """
    Read-only availability report.

    Uses InventoryBatch as the single source of truth.
    StockMovement is audit-only.
    """

    @staticmethod
    def get_available_batches():
        result = []

        batches = InventoryBatch.objects.filter(
            qc_status="APPROVED",
            is_active=True,
            quantity_available__gt=0
        ).select_related("inventory_item")

        for batch in batches:
            result.append({
                "item": batch.inventory_item.name,
                "batch": batch.batch_number,
                "available_qty": batch.quantity_available,
                "expiry_date": batch.expiry_date,
            })

        return result
