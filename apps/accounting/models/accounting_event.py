import uuid
from django.db import models
from apps.accounting.enums import AccountingEventStatus
from apps.accounting.models.journal_entry import JournalEntry


class AccountingEvent(models.Model):
    """
    Accounting Event:
    - Represents a business event requiring accounting
    - Bridges business logic and journal postings
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    event_type = models.CharField(
        max_length=50,
        help_text="Event type (BATCH_CONSUMPTION, GRN_RECEIPT, etc.)"
    )

    source_type = models.CharField(
        max_length=50,
        help_text="Source module (PRODUCTION, INVENTORY, PROCUREMENT)"
    )

    source_reference = models.CharField(
        max_length=100,
        help_text="Source identifier (batch_id, grn_no, etc.)"
    )

    event_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=AccountingEventStatus.choices,
        default=AccountingEventStatus.PENDING
    )

    journal_entry = models.OneToOneField(
        JournalEntry,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="accounting_event"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounting_event"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} | {self.source_reference}"
