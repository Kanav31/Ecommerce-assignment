from django.core.cache import cache
from django.conf import settings

from apps.products.models import Product

PRODUCT_LIST_CACHE_KEY = 'product_list'


class ProductService:

    @staticmethod
    def create_product(user, validated_data: dict) -> Product:
        product = Product.objects.create(
            name       = validated_data['name'],
            price      = validated_data['price'],
            created_by = user,
        )
        cache.delete(PRODUCT_LIST_CACHE_KEY)
        return product

    @staticmethod
    def list_products():
        cached = cache.get(PRODUCT_LIST_CACHE_KEY)
        if cached is not None:
            return cached

        # select_related avoids N+1 when the serializer accesses created_by.name
        products = list(Product.objects.select_related('created_by').all())
        cache.set(PRODUCT_LIST_CACHE_KEY, products, settings.PRODUCT_CACHE_TTL)
        return products
