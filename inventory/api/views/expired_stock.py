from inventory.api.views.base import PaginatedAPIView
from inventory.api.permissions import ReadOnlyInventoryPermission
from inventory.api.serializers.expired_stock import ExpiredStockSerializer
from inventory.reports.expired_stock import expired_stock_report


class ExpiredStockAPIView(PaginatedAPIView):
    permission_classes = [ReadOnlyInventoryPermission]

    def get(self, request):
        report = expired_stock_report()
        expired_batches = report.get("expired", [])

        page, paginator = self.paginate_queryset(expired_batches)
        serializer = ExpiredStockSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
