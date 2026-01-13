# inventory/services/batch_release_service.py

from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError

from inventory.models import InventoryBatch, StockMovement


@transaction.atomic
def release_batch_stock(
    *,
    batch_id: int,
    quantity: Decimal,
    performed_by=None,
    reference: str = None,
    remarks: str = None,
):
    """
    Release previously reserved stock at BATCH level.

    IMPORTANT:
    - This does NOT increase physical stock
    - This only frees up logically reserved quantity
    - Used when plans/orders are cancelled or reduced
    """

    # -----------------------------
    # Basic validation
    # -----------------------------
    if quantity <= 0:
        raise ValidationError("Release quantity must be greater than zero.")

    # -----------------------------
    # Lock batch row (race-safe)
    # -----------------------------
    batch = (
        InventoryBatch.objects
        .select_for_update()
        .get(id=batch_id)
    )

    # -----------------------------
    # Reserved quantity validation
    # -----------------------------
    if quantity > batch.reserved_quantity:
        raise ValidationError(
            f"Cannot release more than reserved. "
            f"Reserved: {batch.reserved_quantity}, "
            f"Requested: {quantity}"
        )

    # -----------------------------
    # Apply logical release
    # -----------------------------
    batch.reserved_quantity -= quantity
    batch.save(update_fields=["reserved_quantity"])

    # -----------------------------
    # Audit log
    # -----------------------------
    StockMovement.objects.create(
        movement_type="RELEASE",
        item=batch.item,          # InventoryItem reference
        quantity=quantity,
        reference=reference,
        performed_by=performed_by,
        remarks=remarks,
    )

    return batch
