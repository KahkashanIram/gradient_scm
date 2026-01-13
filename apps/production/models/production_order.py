import uuid
from django.db import models
from apps.production.enums import ProductionOrderStatus


class ProductionOrder(models.Model):
    """
    Production Order:
    - Created only after Planning APPROVED
    - Defines execution intent
    - Parent of multiple batches
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Traceability
    order_code = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Sales order code"
    )

    # Execution intent
    total_quantity = models.PositiveIntegerField()
    batch_size = models.PositiveIntegerField()
    number_of_batches = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=ProductionOrderStatus.choices,
        default=ProductionOrderStatus.CREATED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "production_order"
        ordering = ["-created_at"]

    def __str__(self):
        return f"PO | {self.order_code} | {self.status}"
