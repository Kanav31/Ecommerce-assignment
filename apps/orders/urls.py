from django.urls import path

from apps.orders.views import OrderListCreateView, AssignDeliveryView, UpdateStatusView

urlpatterns = [
    path('',                       OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:order_id>/assign/',  AssignDeliveryView.as_view(),  name='order-assign-delivery'),
    path('<int:order_id>/status/',  UpdateStatusView.as_view(),    name='order-update-status'),
]
