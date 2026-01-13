from apps.planning.models import PlanningRequest
from apps.sales.models import SalesOrder

def create_planning_request_from_sales(order: SalesOrder) -> PlanningRequest:
    """
    Conservative mapping:
    - Manual call for now
    - No approvals, no checks
    """
    return PlanningRequest.objects.create(
        order_code=order.order_code,
        customer_name=order.customer_name,
        product_id=order.product_id,
        product_description=order.product_description,
        is_new_product=order.is_new_product,
        quantity=order.quantity,
        requested_date=order.requested_date,
        expected_delivery_date=order.expected_delivery_date,
    )
