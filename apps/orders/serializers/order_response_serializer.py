from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemResponseSerializer(serializers.ModelSerializer):
    product_name  = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model        = OrderItem
        fields       = ['id', 'product_id', 'product_name', 'product_price', 'quantity']
        read_only_fields = fields


class OrderResponseSerializer(serializers.ModelSerializer):
    items             = OrderItemResponseSerializer(many=True, read_only=True)
    customer_name     = serializers.CharField(source='customer.name', read_only=True)
    delivery_man_name = serializers.SerializerMethodField()

    class Meta:
        model  = Order
        fields = [
            'id',
            'customer_name',
            'status',
            'delivery_man_name',
            'items',
            'created_at',
        ]
        read_only_fields = fields

    def get_delivery_man_name(self, obj):
        if obj.assigned_delivery_man:
            return obj.assigned_delivery_man.name
        return None
