from rest_framework import serializers
from inventory.models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    performed_by = serializers.StringRelatedField()

    class Meta:
        model = StockMovement
        fields = [
            "movement_type",
            "item",
            "quantity",
            "reference",
            "remarks",
            "performed_by",
            "created_at",
        ]
