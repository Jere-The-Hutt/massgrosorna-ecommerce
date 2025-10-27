from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')


admin.site.register(Category)
