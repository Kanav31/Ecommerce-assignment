from rest_framework import serializers

from apps.orders.serializers.order_item_request_serializer import OrderItemRequestSerializer


class OrderRequestSerializer(serializers.Serializer):
    items = OrderItemRequestSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('Order must contain at least one item.')
        return value
