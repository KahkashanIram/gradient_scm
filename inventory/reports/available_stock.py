from inventory.services.availability_service import InventoryAvailabilityService

def available_stock_report():
    """
    Returns list of all usable inventory
    """
    return InventoryAvailabilityService.get_available_batches()
