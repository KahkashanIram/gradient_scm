from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class StockMovement(models.Model):
    """
    Records logical stock movements (RESERVE / RELEASE).

    IMPORTANT:
    - This model does NOT change stock
    - It only logs intent
    - Actual stock logic lives elsewhere
    """
    """
    Logical stock intent only.

    - RESERVE / RELEASE
    - Does NOT mutate physical stock
    - Used for planning & availability checks
    """

    MOVEMENT_TYPE_CHOICES = (
        ("RESERVE", "Reserve Stock"),
        ("RELEASE", "Release Reserved Stock"),
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPE_CHOICES
    )

    item = models.ForeignKey(
    "inventory.InventoryItem",
    on_delete=models.CASCADE,
    related_name="stock_movements"
)
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        """
        Business validation only.
        NO stock mutation here.
        """
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

    def __str__(self):
        return f"{self.movement_type} | {self.item} | {self.quantity}"
