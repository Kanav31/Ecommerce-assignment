from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers

from apps.accounts.permissions import IsAdmin, IsDeliveryMan
from apps.orders.serializers import OrderResponseSerializer
from apps.orders.services import OrderService


class AssignDeliveryView(APIView):
    """
    POST /api/orders/{id}/assign/
    Admin only — assigns delivery man, sets status → assigned.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        request=inline_serializer(
            name='AssignDeliveryRequest',
            fields={'delivery_man_id': drf_serializers.IntegerField()}
        ),
        responses={200: OrderResponseSerializer},
        tags=['Orders'],
        summary='Assign a delivery man to an order (Admin only)',
    )
    def post(self, request, order_id):
        delivery_man_id = request.data.get('delivery_man_id')
        if not delivery_man_id:
            raise ValidationError('delivery_man_id is required.')

        order = OrderService.assign_delivery(
            order_id=order_id,
            delivery_man_id=delivery_man_id,
        )
        return Response(OrderResponseSerializer(order).data, status=status.HTTP_200_OK)


class UpdateStatusView(APIView):
    """
    PATCH /api/orders/{id}/status/
    Delivery man only — marks assigned order as delivered.
    """
    permission_classes = [IsAuthenticated, IsDeliveryMan]

    @extend_schema(
        request=None,
        responses={200: OrderResponseSerializer},
        tags=['Orders'],
        summary='Mark order as delivered (Delivery Man only)',
    )
    def patch(self, request, order_id):
        order = OrderService.update_status(order_id=order_id, user=request.user)
        return Response(OrderResponseSerializer(order).data, status=status.HTTP_200_OK)
