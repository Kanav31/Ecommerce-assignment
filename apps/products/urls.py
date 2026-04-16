from django.urls import path
from apps.products.views import ProductListCreateView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
]
