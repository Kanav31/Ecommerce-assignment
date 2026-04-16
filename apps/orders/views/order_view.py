from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from apps.accounts.permissions import IsCustomer
from apps.orders.constants import OrderMessage
from apps.orders.serializers import OrderRequestSerializer, OrderResponseSerializer
from apps.orders.services import OrderService
from core.pagination import CustomPageNumberPagination
from core.response import success_response

class OrderListCreateView(APIView):
    """
    GET  /api/orders/ — All authenticated users (role-scoped)
    POST /api/orders/ — Customer only
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    @extend_schema(
        responses={200: OrderResponseSerializer(many=True)},
        tags=['Orders'],
        summary='List orders (role-scoped: admin=all, customer=own, delivery=assigned)',
    )
    def get(self, request):
        orders = OrderService.get_orders_for_user(request.user)
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(orders, request, view=self)
        serializer = OrderResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=OrderRequestSerializer,
        responses={201: OrderResponseSerializer},
        tags=['Orders'],
        summary='Create a new order (Customer only)',
    )
    def post(self, request):
        serializer = OrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = OrderService.create_order(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return success_response(
            message = OrderMessage.ORDER_CREATED,
            status_code = 201,
            data = OrderResponseSerializer(order).data,
        )
