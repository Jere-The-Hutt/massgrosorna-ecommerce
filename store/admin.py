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
        'user',
        'total_price',
        'status',
        'shipping_name',
        'shipping_email',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__username', 'shipping_name', 'shipping_email')

    readonly_fields = ('display_products',)

    fieldsets = (
        (None, {
            'fields': ('user', 'total_price', 'status', 'stripe_payment_intent',
                       'shipping_name', 'shipping_email', 'shipping_address', 'display_products')
        }),
    )

    def display_products(self, obj):
        if not obj.products:
            return "(none)"
        ids = obj.products.split(",")
        titles = []
        for pid in ids:
            try:
                product = Product.objects.get(id=int(pid))
                titles.append(product.title)
            except Product.DoesNotExist:
                titles.append(f"(missing product {pid})")
        return ", ".join(titles)

    display_products.short_description = "Products"


admin.site.register(Category)
