from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from apps.accounting.models import (
    AccountingEvent,
    JournalEntry,
    JournalLine,
    Account,
)
from apps.accounting.enums import AccountingEventStatus


# ============================================================
# POSTING RULES (LOGICAL ROLES, NOT ACCOUNT CODES)
# ============================================================

POSTING_RULES = {
    "GRN_RECEIPT": [
        ("RAW_INVENTORY", "DEBIT"),
        ("GRN_CLEARING", "CREDIT"),
    ],
    "BATCH_CONSUMPTION": [
        ("WIP", "DEBIT"),
        ("RAW_INVENTORY", "CREDIT"),
    ],
    "BATCH_COMPLETION": [
        ("FG_INVENTORY", "DEBIT"),
        ("WIP", "CREDIT"),
    ],
    "BATCH_REJECTION": [
        ("SCRAP_LOSS", "DEBIT"),
        ("WIP", "CREDIT"),
    ],
    # FIXED: Inventory adjustment ALWAYS has two sides
    "INVENTORY_ADJUSTMENT": [
        ("RAW_INVENTORY", "DEBIT_OR_CREDIT"),
        ("INVENTORY_ADJ", "OPPOSITE"),
    ],
}


# ============================================================
# ACCOUNT ROLE → CHART OF ACCOUNT CODE MAPPING
# ============================================================

ACCOUNT_ROLE_MAP = {
    "RAW_INVENTORY": "1100",
    "WIP": "1200",
    "FG_INVENTORY": "1300",
    "GRN_CLEARING": "2100",
    "SCRAP_LOSS": "5100",
    "INVENTORY_ADJ": "5200",
}


# ============================================================
# POSTING SERVICE (ONLY PLACE ALLOWED TO POST ACCOUNTING)
# ============================================================

class PostingService:
    """
    Central Accounting Posting Engine

    Rules:
    - Only this service creates JournalEntry / JournalLine
    - One AccountingEvent → One JournalEntry
    - Posting is atomic and idempotent
    """

    @classmethod
    @transaction.atomic
    def post_event(cls, accounting_event: AccountingEvent, amount: Decimal):
        """
        Convert an AccountingEvent into JournalEntry & JournalLines
        """

        # -----------------------------
        # Guardrails
        # -----------------------------
        if accounting_event.status == AccountingEventStatus.POSTED:
            raise ValueError("AccountingEvent already posted")

        rules = POSTING_RULES.get(accounting_event.event_type)
        if not rules:
            raise ValueError(
                f"No posting rules defined for event type: {accounting_event.event_type}"
            )

        # -----------------------------
        # Create Journal Entry
        # -----------------------------
        journal_entry = JournalEntry.objects.create(
            entry_number=cls._generate_entry_number(),
            entry_date=accounting_event.event_date,
            description=f"{accounting_event.event_type} | {accounting_event.source_reference}",
            source_type=accounting_event.source_type,
            source_reference=accounting_event.source_reference,
            is_posted=True,
        )

        total_debit = Decimal("0.00")
        total_credit = Decimal("0.00")

        # -----------------------------
        # Create Journal Lines
        # -----------------------------
        for role, direction in rules:
            account_code = ACCOUNT_ROLE_MAP.get(role)
            if not account_code:
                raise ValueError(f"No account mapped for role: {role}")

            account = Account.objects.get(account_code=account_code)

            debit = Decimal("0.00")
            credit = Decimal("0.00")

            if direction == "DEBIT":
                debit = amount
                total_debit += debit

            elif direction == "CREDIT":
                credit = amount
                total_credit += credit

            elif direction == "DEBIT_OR_CREDIT":
                if amount >= 0:
                    debit = amount
                    total_debit += debit
                else:
                    credit = abs(amount)
                    total_credit += credit

            elif direction == "OPPOSITE":
                if amount >= 0:
                    credit = amount
                    total_credit += credit
                else:
                    debit = abs(amount)
                    total_debit += debit

            else:
                raise ValueError(f"Unsupported posting direction: {direction}")

            JournalLine.objects.create(
                journal_entry=journal_entry,
                account=account,
                debit=debit,
                credit=credit,
            )

        # -----------------------------
        # Balance Check (NON-NEGOTIABLE)
        # -----------------------------
        if total_debit != total_credit:
            raise ValueError(
                f"Journal not balanced: DR={total_debit} CR={total_credit}"
            )

        # -----------------------------
        # Finalize Accounting Event
        # -----------------------------
        accounting_event.journal_entry = journal_entry
        accounting_event.status = AccountingEventStatus.POSTED
        accounting_event.save()

        return journal_entry

    # ========================================================
    # ENTRY NUMBER GENERATOR
    # ========================================================

    @staticmethod
    def _generate_entry_number():
        """
        Generates sequential journal entry number per day.
        Format: JE-YYYYMMDD-0001
        """
        today = timezone.now().strftime("%Y%m%d")
        count = (
            JournalEntry.objects.filter(
                entry_number__startswith=f"JE-{today}"
            ).count()
            + 1
        )
        return f"JE-{today}-{count:04d}"
