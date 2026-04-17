from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.accounts.permissions import IsAdmin
from apps.products.constants import ProductMessage
from apps.products.serializers import ProductRequestSerializer, ProductResponseSerializer
from apps.products.services import ProductService
from core.pagination import CustomPageNumberPagination
from core.response import success_response


class ProductListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @extend_schema(
        responses={200: ProductResponseSerializer(many=True)},
        tags=['Products'],
        summary='List all products (paginated)',
        parameters=[
            OpenApiParameter('limit', OpenApiTypes.INT, OpenApiParameter.QUERY, description='Number of results to return (max 100)'),
            OpenApiParameter('offset', OpenApiTypes.INT, OpenApiParameter.QUERY, description='Number of results to skip'),
        ],
    )
    def get(self, request):
        products = ProductService.list_products()
        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=ProductRequestSerializer,
        responses={201: ProductResponseSerializer},
        tags=['Products'],
        summary='Create a product (Admin only)',
    )
    def post(self, request):
        serializer = ProductRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = ProductService.create_product(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        return success_response(
            message = ProductMessage.PRODUCT_CREATED,
            status_code = 201,
            data = ProductResponseSerializer(product).data,
        )
