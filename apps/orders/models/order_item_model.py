from django.db import models
from apps.orders.models.order_model import Order
from apps.products.models import Product

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f'{self.quantity}x {self.product.name} (Order #{self.order_id})'
