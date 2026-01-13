# apps/procurement/services/grn_service.py

from datetime import date
from decimal import Decimal

from apps.accounting.models import AccountingEvent
from apps.accounting.services.posting_service import PostingService


def confirm_grn(grn_number: str, total_value: Decimal):
    """
    Called AFTER inventory receipt is completed.

    :param grn_number: GRN reference number
    :param total_value: Total material value received
    """

    # 1️⃣ Create Accounting Event
    event = AccountingEvent.objects.create(
        event_type="GRN_RECEIPT",
        source_type="PROCUREMENT",
        source_reference=grn_number,
        event_date=date.today(),
    )

    # 2️⃣ Post Accounting
    PostingService.post_event(event, total_value)

    return event
