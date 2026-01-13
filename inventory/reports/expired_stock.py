from inventory.services.expiry_service import InventoryExpiryService

def expired_stock_report():
    return {
        "expired": InventoryExpiryService.get_expired(),
        "near_expiry": InventoryExpiryService.get_near_expiry()
    }
