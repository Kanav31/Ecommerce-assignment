from rest_framework import serializers
from apps.orders.constants import OrderItemMessage
from apps.products.models import Product

class OrderItemRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity   = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                OrderItemMessage.PRODUCT_NOT_FOUND.format(product_id=value)
            )
        return value
