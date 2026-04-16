from django.db import transaction
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from apps.accounts.constants import Role
from apps.orders.constants import OrderMessage, Status
from apps.orders.models import Order, OrderItem
from apps.products.models import Product

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, validated_data: dict) -> Order:
        order = Order.objects.create(customer=user)
        order_items = [
            OrderItem(
                order = order,
                product_id = item['product_id'],
                quantity = item['quantity'],
            )
            for item in validated_data['items']
        ]
        OrderItem.objects.bulk_create(order_items)
        return Order.objects.select_related(
            'customer', 'assigned_delivery_man'
        ).prefetch_related('items__product').get(id=order.id)

    @staticmethod
    def get_orders_for_user(user):
        base_qs = Order.objects.select_related(
            'customer', 'assigned_delivery_man'
        ).prefetch_related('items__product')

        if user.role == Role.ADMIN:
            return base_qs.all()
        if user.role == Role.CUSTOMER:
            return base_qs.filter(customer=user)
        if user.role == Role.DELIVERY:
            return base_qs.filter(assigned_delivery_man=user)

        return Order.objects.none()

    @staticmethod
    def assign_delivery(order_id: int, delivery_man_id: int) -> Order:
        from apps.accounts.models import User
        try:
            order = Order.objects.select_related(
                'customer', 'assigned_delivery_man'
            ).prefetch_related('items__product').get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(OrderMessage.ORDER_NOT_FOUND.format(order_id=order_id))
        try:
            delivery_man = User.objects.get(id=delivery_man_id, role=Role.DELIVERY)
        except User.DoesNotExist:
            raise NotFound(OrderMessage.DELIVERY_MAN_NOT_FOUND)

        if order.status == Status.DELIVERED:
            raise ValidationError(OrderMessage.ALREADY_DELIVERED)

        order.assigned_delivery_man = delivery_man
        order.status = Status.ASSIGNED
        order.save(update_fields=['assigned_delivery_man', 'status'])

        return order

    @staticmethod
    def update_status(order_id: int, user) -> Order:
        try:
            order = Order.objects.select_related(
                'customer', 'assigned_delivery_man'
            ).prefetch_related('items__product').get(id=order_id)
        except Order.DoesNotExist:
            raise NotFound(OrderMessage.ORDER_NOT_FOUND.format(order_id=order_id))

        if order.assigned_delivery_man_id != user.id:
            raise PermissionDenied(OrderMessage.NOT_ASSIGNED_TO_ORDER)

        if order.status != Status.ASSIGNED:
            raise ValidationError(
                OrderMessage.INVALID_STATUS_TRANSITION.format(status=order.status)
            )
        order.status = Status.DELIVERED
        order.save(update_fields=['status'])

        return order
