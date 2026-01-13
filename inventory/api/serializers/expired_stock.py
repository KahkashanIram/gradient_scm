from rest_framework import serializers


class ExpiredStockSerializer(serializers.Serializer):
    item = serializers.CharField(source="inventory_item")
    batch = serializers.CharField(source="batch_number")
    expiry_date = serializers.DateField()
    qc_status = serializers.CharField()
    quantity_available = serializers.DecimalField(
        max_digits=12, decimal_places=3
    )
