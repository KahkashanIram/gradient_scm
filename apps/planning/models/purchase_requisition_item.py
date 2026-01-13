import uuid
from django.db import models
from apps.planning.models.purchase_requisition import PurchaseRequisition


class PurchaseRequisitionItem(models.Model):
    """
    Purchase Requisition Item:
    - Represents a shortage item
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # Inventory-agnostic
    item_code = models.CharField(max_length=50)
    unit_of_measure = models.CharField(max_length=20)

    quantity_required = models.DecimalField(
        max_digits=12, decimal_places=3,
        help_text="Quantity to procure"
    )

    class Meta:
        db_table = "purchase_requisition_item"

    def __str__(self):
        return f"{self.item_code} | {self.quantity_required} {self.unit_of_measure}"
