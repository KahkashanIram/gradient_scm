import uuid
from django.db import models
from apps.planning.enums import PlanningStatus


class PlanningRequest(models.Model):
    """
    Conservative PlanningRequest:
    - Snapshot of SalesOrder at submit time
    - Created by system
    - Planning owns approve / reject decisions
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Global trace (links back to SalesOrder)
    order_code = models.CharField(max_length=30, db_index=True)

    # Context (no masters enforced)
    customer_name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.TextField()
    is_new_product = models.BooleanField(default=False)

    # Demand snapshot
    quantity = models.PositiveIntegerField()
    requested_date = models.DateField()
    expected_delivery_date = models.DateField()

    # 🔐 Planning decision state
    status = models.CharField(
        max_length=20,
        choices=PlanningStatus.choices,
        default=PlanningStatus.PENDING
    )

    # Decision audit (ONLY set on approve / reject)
    decision_reason = models.TextField(null=True, blank=True)
    decided_by = models.CharField(max_length=100, null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "planning_request"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_code} | {self.status}"
