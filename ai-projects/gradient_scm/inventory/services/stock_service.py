# inventory/services/stock_service.py

from django.db import transaction
from django.core.exceptions import ValidationError

from inventory.models.batch import InventoryBatch
from inventory.models.stock_movement import StockMovement


@transaction.atomic
def reserve_stock(batch: InventoryBatch, quantity: float, reference=None, user=None):
    """
    Reserve stock from a batch.

    Rules:
    - Batch must be ACTIVE
    - quantity > 0
    - quantity <= available (quantity_available - reserved_quantity)
    """

    if not batch.is_active:
        raise ValidationError("Cannot reserve stock from inactive batch.")

    if quantity <= 0:
        raise ValidationError("Reserve quantity must be greater than zero.")

    available_to_reserve = batch.quantity_available - batch.reserved_quantity

    if quantity > available_to_reserve:
        raise ValidationError("Not enough available stock to reserve.")

    # Update reservation
    batch.reserved_quantity += quantity
    batch.save()

    # Audit log (optional but recommended)
    StockMovement.objects.create(
        movement_type="RESERVE",
        item=batch.inventory_item,
        quantity=quantity,
        reference=reference,
        performed_by=user,
        remarks=f"Reserved from batch {batch.batch_number}",
    )


@transaction.atomic
def release_stock(batch: InventoryBatch, quantity: float, reference=None, user=None):
    """
    Release previously reserved stock.

    Rules:
    - quantity > 0
    - quantity <= reserved_quantity
    """

    if quantity <= 0:
        raise ValidationError("Release quantity must be greater than zero.")

    if quantity > batch.reserved_quantity:
        raise ValidationError("Cannot release more than reserved quantity.")

    # Update reservation
    batch.reserved_quantity -= quantity
    batch.save()

    # Audit log
    StockMovement.objects.create(
        movement_type="RELEASE",
        item=batch.inventory_item,
        quantity=quantity,
        reference=reference,
        performed_by=user,
        remarks=f"Released from batch {batch.batch_number}",
    )
@transaction.atomic
def consume_stock(batch, quantity, reference=None, user=None):
    """
    Consume stock from RESERVED quantity.

    Rules:
    - Batch must be ACTIVE
    - quantity > 0
    - quantity <= reserved_quantity
    """

    if not batch.is_active:
        raise ValidationError("Cannot consume stock from inactive batch.")

    if quantity <= 0:
        raise ValidationError("Consume quantity must be greater than zero.")

    if quantity > batch.reserved_quantity:
        raise ValidationError("Cannot consume more than reserved quantity.")

    # Apply consumption
    batch.reserved_quantity -= quantity
    batch.quantity_available -= quantity
    batch.save()

    # Audit log
    StockMovement.objects.create(
        movement_type="CONSUME",
        item=batch.inventory_item,
        quantity=quantity,
        reference=reference,
        performed_by=user,
        remarks=f"Consumed from batch {batch.batch_number}",
    )