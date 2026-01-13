import uuid
from django.db import models
from apps.qc.enums import QCRecipeStatus
from apps.production.models.production_batch import ProductionBatch


class QCRecipe(models.Model):
    """
    QC Recipe (per batch):
    - One recipe per ProductionBatch
    - Defines technical composition only
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link to execution unit
    batch = models.OneToOneField(
        ProductionBatch,
        on_delete=models.CASCADE,
        related_name="qc_recipe"
    )

    status = models.CharField(
        max_length=20,
        choices=QCRecipeStatus.choices,
        default=QCRecipeStatus.DRAFT
    )

    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "qc_recipe"
        ordering = ["-created_at"]

    def __str__(self):
        return f"QCRecipe | {self.batch.batch_id} | {self.status}"
