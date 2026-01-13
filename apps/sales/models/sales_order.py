import uuid
from django.db import models
from apps.sales.enums import SalesOrderStatus


class SalesOrder(models.Model):
    """
    Conservative SalesOrder:
    - Captures sales intent
    - Generates order_code on submit
    - No decision logic
    - Mirrors Planning decision (read-only)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Business identity (generated on submit)
    order_code = models.CharField(
        max_length=30, unique=True, null=True, blank=True, db_index=True
    )

    # Customer & product intent (no masters yet)
    customer_name = models.CharField(max_length=255)

    product_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Short business-friendly product name"
    )

    product_id = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.TextField()
    is_new_product = models.BooleanField(default=False)

    # Demand
    quantity = models.PositiveIntegerField()
    requested_date = models.DateField()
    expected_delivery_date = models.DateField()

    # Sales lifecycle (Sales-owned)
    status = models.CharField(
        max_length=20,
        choices=SalesOrderStatus.choices,
        default=SalesOrderStatus.DRAFT
    )

    # 🔁 Planning decision mirror (READ-ONLY for Sales)
    planning_status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Mirror of PlanningRequest.status"
    )

    planning_decision_reason = models.TextField(
        null=True,
        blank=True,
        help_text="Reason provided by Planning if order is rejected"
    )

    planning_decided_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when Planning approved/rejected the order"
    )

    # Audit
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sales_order"
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_code or str(self.id)
