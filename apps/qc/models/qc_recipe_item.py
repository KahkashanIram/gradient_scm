import uuid
from django.db import models
from apps.qc.models.qc_recipe import QCRecipe


class QCRecipeItem(models.Model):
    """
    QC Recipe Item:
    - Item-level composition for a batch
    - Quantity is PER BATCH
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    recipe = models.ForeignKey(
        QCRecipe,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # Inventory-agnostic identifiers
    item_code = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255, blank=True)

    unit_of_measure = models.CharField(max_length=20)
    quantity_required = models.DecimalField(
        max_digits=12, decimal_places=3,
        help_text="Quantity required per batch"
    )

    class Meta:
        db_table = "qc_recipe_item"

    def __str__(self):
        return f"{self.item_code} | {self.quantity_required} {self.unit_of_measure}"
