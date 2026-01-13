from django.db import transaction
from django.utils import timezone
from django.db.models import Max

from apps.sales.models.sales_order import SalesOrder
from apps.sales.enums import SalesOrderStatus

# Fan-out consumers (system responsibility — used later)
from apps.planning.services.planning_service import (
    create_planning_request_from_sales
)
from apps.rd.services.rd_service import (
    create_new_product_request_from_sales
)


def generate_order_code():
    """
    Generate system Sales Order Code

    Format:
        SO-YYYYMM-XXXXX
        Example: SO-202601-00001
    """

    prefix = timezone.now().strftime("SO-%Y%m")

    last_order_code = (
        SalesOrder.objects
        .filter(order_code__startswith=prefix)
        .aggregate(max_code=Max("order_code"))
        .get("max_code")
    )

    if last_order_code:
        last_seq = int(last_order_code.split("-")[-1])
        next_seq = last_seq + 1
    else:
        next_seq = 1

    return f"{prefix}-{next_seq:05d}"


def assign_order_code(order: SalesOrder):
    """
    Assign order_code at creation time (Phase D0/D1)

    - Order must be DRAFT
    - No fan-out
    - No status change
    """

    if order.order_code:
        return order  # already assigned (safety)

    if order.status != SalesOrderStatus.DRAFT:
        raise ValueError("Order code can only be assigned to DRAFT orders")

    order.order_code = generate_order_code()
    order.save(update_fields=["order_code", "updated_at"])

    return order


def submit_sales_order(order: SalesOrder):
    """
    Submit Sales Order (Phase D3+)

    Responsibilities:
    - Validate DRAFT state
    - Lock order (SUBMITTED)
    - Fan-out to Planning (always)
    - Fan-out to R&D (only if is_new_product=True)

    Sales exits the process here.
    """

    if order.status != SalesOrderStatus.DRAFT:
        raise ValueError("Only DRAFT sales orders can be submitted")

    with transaction.atomic():
        # Ensure order code exists
        if not order.order_code:
            order.order_code = generate_order_code()

        # Lock order
        order.status = SalesOrderStatus.SUBMITTED
        order.save(update_fields=["order_code", "status", "updated_at"])

        # System fan-out (NO business decisions here)
        create_planning_request_from_sales(order)
        create_new_product_request_from_sales(order)  # safe no-op if not new

    return order
