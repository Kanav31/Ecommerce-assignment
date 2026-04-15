from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Shows OrderItems directly inside the Order edit page in Django admin.
    TabularInline renders them as a table — cleaner than StackedInline
    for simple models with few fields.
    """
    model  = OrderItem
    extra  = 0  # don't show empty extra rows
    fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'customer', 'status', 'assigned_delivery_man', 'created_at')
    list_filter   = ('status',)
    search_fields = ('customer__email',)
    ordering      = ('-created_at',)
    inlines       = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
