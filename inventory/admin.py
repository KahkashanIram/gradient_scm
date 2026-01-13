from django.contrib import admin
from inventory.models.batch import InventoryBatch
from inventory.models.item_master import InventoryItem
from inventory.models.stock_movement import StockMovement


# =========================================================
# INVENTORY ITEM ADMIN
# =========================================================
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """
    InventoryItem admin.

    Rules:
    - created_by is auto-set from logged-in user
    - created_by is hidden on ADD
    - created_by is read-only on CHANGE
    """

    list_display = (
        "item_code",
        "item_name",
        "item_status",
        "is_active",
    )

    search_fields = (
        "item_code",
        "item_name",
    )

    list_filter = (
        "item_status",
        "inventory_nature",
        "inventory_usage",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_fields(self, request, obj=None):
        fields = [
            "item_code",
            "item_name",
            "description",
            "inventory_nature",
            "inventory_usage",
            "procurement_type",
            "hazard_class",
            "shelf_life_days",
            "expiry_tracking_required",
            "item_status",
            "approved_by",
            "approved_on",
        ]

        if obj:
            fields.insert(fields.index("approved_by"), "created_by")

        return fields

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("created_by",)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# # =========================================================
# # INVENTORY BATCH ADMIN (FINAL)
# # =========================================================
@admin.register(InventoryBatch)
class InventoryBatchAdmin(admin.ModelAdmin):
    """
    InventoryBatch admin.

    FINAL RULES:
    - Batch = metadata + QC state
    - NO manual stock editing in admin
    - Quantities are system-managed (GRN / Reserve / Consume)
    """

    # -----------------------------
    # List view
    # -----------------------------
    list_display = (
        "batch_number",
        "inventory_item",
        "qc_status",
        "is_active",
        "expiry_date",
        "created_at",
    )

    search_fields = (
        "batch_number",
        "inventory_item__item_code",
        "inventory_item__item_name",
    )

    list_filter = (
        "qc_status",
        "is_active",
        "expiry_date",
    )

    # -----------------------------
    # Read-only system fields
    # -----------------------------
    readonly_fields = (
        "is_active",
        "expiry_date",
        "created_at",
    )

    # -----------------------------
    # Form layout
    # -----------------------------
    fieldsets = (
        (
            "Batch Information",
            {
                "fields": (
                    "inventory_item",
                    "batch_number",
                    "receiving_date",
                )
            },
        ),
        (
            "Quality Control",
            {
                "fields": (
                    "qc_status",
                    "is_active",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "expiry_date",
                    "created_at",
                )
            },
        ),
    )

    # -----------------------------
    # Permissions
    # -----------------------------
    def has_change_permission(self, request, obj=None):
        """
        Allow editing ONLY while QC is pending.
        """
        if obj and obj.qc_status != "QC_PENDING":
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Never allow deletion of batches (audit safety).
        """
        return False


# # =========================================================
# # STOCK MOVEMENT ADMIN (AUDIT-ONLY, FINAL)
# # =========================================================
# @admin.register(StockMovement)
# class StockMovementAdmin(admin.ModelAdmin):
#     """
#     StockMovement admin.

#     FINAL RULES:
#     - Audit log only
#     - No create / edit / delete
#     """

#     list_display = (
#         "id",
#         "movement_type",
#         "item",
#         "quantity",
#         "reference",
#         "performed_by",
#         "created_at",
#     )

#     list_filter = (
#         "movement_type",
#         "created_at",
#     )

#     search_fields = (
#         "reference",
#         "item__item_code",
#         "item__item_name",
#     )

#     readonly_fields = (
#         "movement_type",
#         "item",
#         "quantity",
#         "reference",
#         "performed_by",
#         "remarks",
#         "created_at",
#     )

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False
