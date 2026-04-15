from rest_framework import serializers


class ProductRequestSerializer(serializers.Serializer):
    """Validates POST /api/products/ — created_by is set from request.user, not accepted here."""
    name  = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than zero.')
        return value
