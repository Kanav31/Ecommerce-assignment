from rest_framework import serializers

from apps.products.models import Product


class ProductResponseSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = ['id', 'name', 'price', 'created_by_name', 'created_at']
        read_only_fields = fields

    def get_created_by_name(self, obj):
        return obj.created_by.name
