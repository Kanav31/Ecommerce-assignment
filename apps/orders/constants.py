from django.db import models

class Status(models.TextChoices):
    PENDING   = 'pending',   'Pending'
    ASSIGNED  = 'assigned',  'Assigned'
    DELIVERED = 'delivered', 'Delivered'

class OrderMessage:
    # Success messages
    ORDER_CREATED     = 'Order created successfully.'
    DELIVERY_ASSIGNED = 'Delivery man assigned successfully.'
    ORDER_DELIVERED   = 'Order marked as delivered successfully.'

    # Error messages — use .format(order_id=...) / .format(status=...) for dynamic ones
    DELIVERY_MAN_ID_REQUIRED  = 'delivery_man_id is required.'
    ORDER_NOT_FOUND           = 'Order with id {order_id} not found.'
    DELIVERY_MAN_NOT_FOUND    = 'Delivery man not found or user is not a delivery man.'
    ALREADY_DELIVERED         = 'Cannot assign a delivery man to an already delivered order.'
    NOT_ASSIGNED_TO_ORDER     = 'You are not assigned to this order.'
    INVALID_STATUS_TRANSITION = 'Order cannot be marked as delivered. Current status: {status}'
    ITEMS_REQUIRED            = 'Order must contain at least one item.'

class OrderItemMessage:
    PRODUCT_NOT_FOUND = 'Product with id {product_id} does not exist.'
