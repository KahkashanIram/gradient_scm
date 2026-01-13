from apps.rd.models import NewProductRequest
from apps.sales.models import SalesOrder

def create_new_product_request_from_sales(order: SalesOrder) -> NewProductRequest | None:
    """
    Create R&D intake only if product is new.
    Conservative: manual call for now.
    """
    if not order.is_new_product:
        return None

    return NewProductRequest.objects.create(
        order_code=order.order_code,
        product_description=order.product_description,
        customer_name=order.customer_name,
    )
