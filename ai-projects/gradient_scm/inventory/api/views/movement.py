from inventory.api.views.base import PaginatedAPIView
from inventory.api.permissions import ReadOnlyInventoryPermission
from inventory.api.serializers.movement import StockMovementSerializer
from inventory.models import StockMovement


class InventoryMovementAPIView(PaginatedAPIView):
    permission_classes = [ReadOnlyInventoryPermission]

    def get(self, request):
        qs = StockMovement.objects.all().order_by("-created_at")

        page, paginator = self.paginate_queryset(qs)
        serializer = StockMovementSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
