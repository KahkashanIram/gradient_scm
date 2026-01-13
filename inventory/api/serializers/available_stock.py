from rest_framework import serializers

class AvailableStockSerializer(serializers.Serializer):
    item = serializers.CharField()
    batch = serializers.CharField()
    available_qty = serializers.DecimalField(max_digits=12, decimal_places=3)
    expiry_date = serializers.DateField()
