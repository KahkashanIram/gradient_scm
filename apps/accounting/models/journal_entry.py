import uuid
from django.db import models


class JournalEntry(models.Model):
    """
    Journal Entry (JE):
    - Represents a single accounting event
    - Groups debit & credit lines
    - Immutable after posting
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    entry_number = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        help_text="System generated journal entry number"
    )

    entry_date = models.DateField()

    description = models.TextField()

    source_type = models.CharField(
        max_length=50,
        help_text="Source document type (BATCH, GRN, INVENTORY, etc.)"
    )

    source_reference = models.CharField(
        max_length=100,
        help_text="Source reference ID (batch_id, grn_no, etc.)"
    )

    is_posted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "journal_entry"
        ordering = ["-created_at"]

    def __str__(self):
        return f"JE {self.entry_number}"
