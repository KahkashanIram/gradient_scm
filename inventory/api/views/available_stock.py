from datetime import datetime
from inventory.api.views.base import PaginatedAPIView
from inventory.api.permissions import ReadOnlyInventoryPermission
from inventory.api.serializers.available_stock import AvailableStockSerializer
from inventory.reports.available_stock import available_stock_report


class AvailableStockAPIView(PaginatedAPIView):
    permission_classes = [ReadOnlyInventoryPermission]

    def get(self, request):
        data = available_stock_report()

        # --- Filters ---
        item = request.query_params.get("item")
        batch = request.query_params.get("batch")
        expiry_before = request.query_params.get("expiry_before")
        expiry_after = request.query_params.get("expiry_after")

        if item:
            data = [d for d in data if d["item"] == item]

        if batch:
            data = [d for d in data if d["batch"] == batch]

        if expiry_before:
            before_date = datetime.strptime(
                expiry_before, "%Y-%m-%d"
            ).date()
            data = [
                d for d in data
                if d["expiry_date"] and d["expiry_date"] <= before_date
            ]

        if expiry_after:
            after_date = datetime.strptime(
                expiry_after, "%Y-%m-%d"
            ).date()
            data = [
                d for d in data
                if d["expiry_date"] and d["expiry_date"] >= after_date
            ]

        page, paginator = self.paginate_queryset(data)
        serializer = AvailableStockSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
