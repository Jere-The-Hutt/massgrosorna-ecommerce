from django.contrib import admin
from .models import Product, Category, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'user',
        'total_price',
        'status',
        'created_at'
        )
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'product__title', 'user__username')


admin.site.register(Category)
