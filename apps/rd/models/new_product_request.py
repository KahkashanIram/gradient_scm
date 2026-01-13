import uuid
from django.db import models

class NewProductRequest(models.Model):
    """
    R&D Intake Queue (Stub):
    - Created when SalesOrder.is_new_product = True
    - Not a Product Master
    - No approvals or definitions here
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Traceability
    order_code = models.CharField(max_length=30, db_index=True)

    # What Sales asked for (verbatim)
    product_description = models.TextField()

    # Optional context
    customer_name = models.CharField(max_length=255, blank=True)

    # R&D intake state
    status = models.CharField(
        max_length=20,
        default="OPEN"   # later: IN_REVIEW / DEFINED / REJECTED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rd_new_product_request"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_code} | {self.status}"
