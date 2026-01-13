import uuid
from django.db import models
from apps.production.models.production_order import ProductionOrder


class ProductionBatch(models.Model):
    """
    Production Batch:
    - Smallest execution unit
    - Auto-generated batch_id
    - Linked to ProductionOrder
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    production_order = models.ForeignKey(
        ProductionOrder,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    batch_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    status = models.CharField(
        max_length=20,
        default="CREATED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "production_batch"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.batch_id} | {self.status}"
