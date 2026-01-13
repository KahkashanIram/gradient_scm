import uuid
from django.db import models
from apps.accounting.enums import AccountType


class Account(models.Model):
    """
    Chart of Accounts (COA)

    - Static master data
    - Used by JournalLines
    - No balances stored here
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    account_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique account code (e.g. 1100, 5001)"
    )

    account_name = models.CharField(
        max_length=255,
        help_text="Account name (e.g. Raw Material Inventory)"
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices
    )

    parent_account = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        help_text="Optional parent account for hierarchy"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "account"
        ordering = ["account_code"]

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"
