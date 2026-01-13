from datetime import date
from decimal import Decimal

from apps.accounting.models import AccountingEvent
from apps.accounting.services.posting_service import PostingService


def consume_batch_material(batch_id: str, total_material_cost: Decimal):
    """
    Called AFTER inventory has issued materials for a batch.

    Accounting Impact:
    DR Work In Progress (WIP)
    CR Raw Material Inventory
    """

    # 1️⃣ Create Accounting Event
    event = AccountingEvent.objects.create(
        event_type="BATCH_CONSUMPTION",
        source_type="PRODUCTION",
        source_reference=batch_id,
        event_date=date.today(),
    )

    # 2️⃣ Post Accounting
    PostingService.post_event(event, total_material_cost)

    return event


def complete_batch(batch_id: str, batch_total_cost: Decimal):
    """
    Called AFTER batch production is completed and FG inventory is received.

    Accounting Impact:
    DR Finished Goods Inventory
    CR Work In Progress (WIP)
    """

    # 1️⃣ Create Accounting Event
    event = AccountingEvent.objects.create(
        event_type="BATCH_COMPLETION",
        source_type="PRODUCTION",
        source_reference=batch_id,
        event_date=date.today(),
    )

    # 2️⃣ Post Accounting
    PostingService.post_event(event, batch_total_cost)

    return event
