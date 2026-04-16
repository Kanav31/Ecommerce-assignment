from django.db import models
from django.conf import settings
from django.core.cache import cache
from apps.products.constants import PRODUCT_LIST_CACHE_KEY

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='products',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(PRODUCT_LIST_CACHE_KEY)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete(PRODUCT_LIST_CACHE_KEY)

    def __str__(self):
        return f'{self.name} (₹{self.price})'
