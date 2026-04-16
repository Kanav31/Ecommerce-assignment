from django.core.cache import cache
from django.conf import settings
from apps.products.constants import PRODUCT_LIST_CACHE_KEY
from apps.products.models import Product

class ProductService:
    @staticmethod
    def create_product(user, validated_data: dict) -> Product:
        return Product.objects.create(
            name = validated_data['name'],
            price = validated_data['price'],
            created_by = user,
        )

    @staticmethod
    def list_products():
        cached = cache.get(PRODUCT_LIST_CACHE_KEY)
        if cached is not None:
            return cached

        products = list(Product.objects.select_related('created_by').all())
        cache.set(PRODUCT_LIST_CACHE_KEY, products, settings.PRODUCT_CACHE_TTL)
        return products
