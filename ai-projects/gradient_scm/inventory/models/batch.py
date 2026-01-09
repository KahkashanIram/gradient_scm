from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from inventory.models.item_master import InventoryItem
from inventory.constants import QCStatus


class InventoryBatch(models.Model):
    """
    Inventory Batch

    Represents a physical batch of inventory.
    Quantities are system-managed (GRN / Reserve / Consume),
    NOT edited manually in admin.
    """

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.PROTECT,
        related_name="batches",
    )

    batch_number = models.CharField(
        max_length=100
    )

    receiving_date = models.DateField(
        default=now
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    # 🔒 Database-safe fields (match existing schema)
    quantity_received = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0
    )

    quantity_available = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0
    )

    reserved_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0
    )

    qc_status = models.CharField(
        max_length=20,
        choices=QCStatus.choices,
        default=QCStatus.QC_PENDING
    )

    is_active = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # ==========================
    # VALIDATION
    # ==========================
    def clean(self):
        if not self.inventory_item.is_active:
            raise ValidationError(
                "Cannot create batch for inactive inventory item."
            )

        if self.quantity_received < 0:
            raise ValidationError(
                "Received quantity cannot be negative."
            )

        if self.quantity_available < 0:
            raise ValidationError(
                "Available quantity cannot be negative."
            )

        if self.reserved_quantity < 0:
            raise ValidationError(
                "Reserved quantity cannot be negative."
            )

        if self.reserved_quantity > self.quantity_available:
            raise ValidationError(
                "Reserved quantity cannot exceed available quantity."
            )

    # ==========================
    # SAVE LOGIC
    # ==========================
    def save(self, *args, **kwargs):
        # Auto-calculate expiry date
        if (
            self.inventory_item.expiry_tracking_required
            and self.inventory_item.shelf_life_days
            and not self.expiry_date
        ):
            self.expiry_date = (
                self.receiving_date
                + timedelta(days=self.inventory_item.shelf_life_days)
            )

        # Expiry handling
        if self.expiry_date and self.expiry_date < now().date():
            self.qc_status = QCStatus.EXPIRED
            self.is_active = False
        else:
            self.is_active = self.qc_status == QCStatus.QC_APPROVED

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-receiving_date"]
        unique_together = ("inventory_item", "batch_number")

    def __str__(self):
        return f"{self.inventory_item.item_code} | Batch {self.batch_number}"
