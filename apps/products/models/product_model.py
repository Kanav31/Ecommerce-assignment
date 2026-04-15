from django.db import models
from django.conf import settings


class Product(models.Model):
    name       = models.CharField(max_length=255)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # prevent deleting an admin who has products
        related_name='products',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} (₹{self.price})'
