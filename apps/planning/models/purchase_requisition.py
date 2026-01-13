import uuid
from django.db import models
from apps.planning.enums import PurchaseRequisitionStatus


class PurchaseRequisition(models.Model):
    """
    Purchase Requisition:
    - Created by Planning from shortages
    - Internal authorization to buy
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Context
    order_code = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Sales order code"
    )

    production_order_id = models.UUIDField(
        help_text="Linked ProductionOrder ID"
    )

    status = models.CharField(
        max_length=20,
        choices=PurchaseRequisitionStatus.choices,
        default=PurchaseRequisitionStatus.CREATED
    )

    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "purchase_requisition"
        ordering = ["-created_at"]

    def __str__(self):
        return f"PR | {self.order_code} | {self.status}"
