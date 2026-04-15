from django.contrib import admin

from apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'created_by', 'created_at')
    list_filter   = ('created_by',)
    search_fields = ('name',)
    ordering      = ('-created_at',)
