class Status:
    """
    Order status lifecycle:
    PENDING → order created by customer, not yet assigned
    ASSIGNED → admin assigned a delivery man
    DELIVERED → delivery man marked as delivered
    """
    PENDING   = 'pending'
    ASSIGNED  = 'assigned'
    DELIVERED = 'delivered'

    CHOICES = [
        (PENDING,   'Pending'),
        (ASSIGNED,  'Assigned'),
        (DELIVERED, 'Delivered'),
    ]
