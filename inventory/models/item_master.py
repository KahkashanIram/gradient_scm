# inventory/models/item_master.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class InventoryItem(models.Model):
    """
    Inventory Master Item

    This represents the APPROVED definition of an inventory item.
    Physical stock always lives at InventoryBatch level.
    """

    # =========================================================
    # IDENTIFICATION
    # =========================================================
    item_code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique inventory item code"
    )

    item_name = models.CharField(
        max_length=255,
        help_text="Human readable item name"
    )

    description = models.TextField(
        blank=True
    )

    # =========================================================
    # CLASSIFICATION
    # =========================================================
    inventory_nature = models.CharField(
        max_length=50,
        choices=[
            ("RAW", "Raw Material"),
            ("PACK", "Packaging"),
            ("FG", "Finished Goods"),
        ]
    )

    inventory_usage = models.CharField(
        max_length=50,
        choices=[
            ("OPERATIONAL", "Operational"),
            ("TECHNICAL", "Technical"),
            ("SALE", "For Sale"),
        ]
    )

    procurement_type = models.CharField(
        max_length=50,
        choices=[
            ("PURCHASED", "Purchased"),
            ("MANUFACTURED", "Manufactured"),
        ]
    )

    hazard_class = models.CharField(
        max_length=50,
        choices=[
            ("NONE", "Non Hazardous"),
            ("FLAMMABLE", "Flammable"),
            ("TOXIC", "Toxic"),
            ("CORROSIVE", "Corrosive"),
        ],
        blank=True
    )

    # =========================================================
    # SHELF LIFE
    # =========================================================
    shelf_life_days = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Shelf life in days"
    )

    expiry_tracking_required = models.BooleanField(
        default=False
    )

    # =========================================================
    # STATUS & APPROVAL
    # =========================================================
    item_status = models.CharField(
        max_length=20,
        choices=[
            ("Draft", "Draft"),
            ("Active", "Active"),
            ("Deprecated", "Deprecated"),
        ],
        default="Draft"
    )

    # ⚠️ SYSTEM DERIVED — DO NOT EDIT MANUALLY
    is_active = models.BooleanField(
        default=False,
        help_text="System derived. Do not edit manually."
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="approved_inventory_items"
    )

    approved_on = models.DateTimeField(
        null=True,
        blank=True
    )

    # =========================================================
    # AUDIT
    # =========================================================
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_inventory_items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # VALIDATION
    # =========================================================
    def clean(self):
        """
        Model-level integrity rules.
        """

        if self.expiry_tracking_required and not self.shelf_life_days:
            raise ValidationError(
                "Shelf life days must be set if expiry tracking is required."
            )

    # =========================================================
    # SAVE LOGIC (SOURCE OF TRUTH)
    # =========================================================
    def save(self, *args, **kwargs):
        """
        Enforce system-derived activation logic.
        """

        # Enforce created_by on first save
        if self.pk is None and self.created_by is None:
            raise ValidationError(
                "created_by must be set before saving InventoryItem."
            )

        # 🔑 SYSTEM-DERIVED is_active
        self.is_active = (
            self.item_status == "Active"
            and self.approved_by is not None
            and self.approved_on is not None
        )

        super().save(*args, **kwargs)

    # =========================================================
    # META
    # =========================================================
    class Meta:
        ordering = ["item_code"]
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    def __str__(self):
        return f"{self.item_code} - {self.item_name}"
