from datetime import date
from decimal import Decimal

from apps.accounting.models import AccountingEvent
from apps.accounting.services.posting_service import PostingService


def post_inventory_adjustment(
    adjustment_ref: str,
    adjustment_value: Decimal,
):
    """
    Accounting integration for inventory adjustments.

    IMPORTANT:
    - Inventory quantity must already be updated BEFORE calling this
    - This function ONLY handles accounting
    """

    event = AccountingEvent.objects.create(
        event_type="INVENTORY_ADJUSTMENT",
        source_type="INVENTORY",
        source_reference=adjustment_ref,
        event_date=date.today(),
    )

    PostingService.post_event(event, adjustment_value)

    return event
