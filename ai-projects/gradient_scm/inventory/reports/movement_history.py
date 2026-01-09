from inventory.services.movement_service import InventoryMovementService

def inventory_movement_report(filters=None):
    filters = filters or {}
    return InventoryMovementService.get_history(
        item=filters.get("item"),
        batch=filters.get("batch")
    )
