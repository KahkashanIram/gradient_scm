# inventory/services/batch_reserve_service.py

from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError

from inventory.models import InventoryBatch, StockMovement


@transaction.atomic
def reserve_batch_stock(
    *,
    batch_id: int,
    quantity: Decimal,
    performed_by=None,
    reference: str = None,
    remarks: str = None,
):
    """
    Reserve stock at BATCH level (logical reservation).

    IMPORTANT:
    - This does NOT reduce physical stock
    - This only blocks stock for planning / sales / production
    - Physical stock remains unchanged until CONSUME
    """

    # -----------------------------
    # Basic validation
    # -----------------------------
    if quantity <= 0:
        raise ValidationError("Reservation quantity must be greater than zero.")

    # -----------------------------
    # Lock batch row (race-safe)
    # -----------------------------
    batch = (
        InventoryBatch.objects
        .select_for_update()
        .get(id=batch_id)
    )

    if not batch.is_active:
        raise ValidationError(
            "Cannot reserve stock from inactive or expired batch."
        )

    # -----------------------------
    # Available stock calculation
    # -----------------------------
    available_for_reserve = (
        batch.quantity_available - batch.reserved_quantity
    )

    if quantity > available_for_reserve:
        raise ValidationError(
            f"Insufficient stock to reserve. "
            f"Available: {available_for_reserve}, "
            f"Requested: {quantity}"
        )

    # -----------------------------
    # Apply logical reservation
    # -----------------------------
    batch.reserved_quantity += quantity
    batch.save(update_fields=["reserved_quantity"])

    # -----------------------------
    # Audit log
    # -----------------------------
    StockMovement.objects.create(
        movement_type="RESERVE",
        item=batch.item,          # InventoryItem reference
        quantity=quantity,
        reference=reference,
        performed_by=performed_by,
        remarks=remarks,
    )

    return batch
