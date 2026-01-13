import uuid
from django.db import models
from apps.accounting.models.account import Account
from apps.accounting.models.journal_entry import JournalEntry


class JournalLine(models.Model):
    """
    Journal Line:
    - Debit or Credit line
    - Always linked to a JournalEntry
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="lines"
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="journal_lines"
    )

    debit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "journal_line"

    def __str__(self):
        return f"{self.account.account_code} | DR {self.debit} CR {self.credit}"
