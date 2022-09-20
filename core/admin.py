from django.contrib import admin

from core.models import Product, Category, PriceHistory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(PriceHistory)
