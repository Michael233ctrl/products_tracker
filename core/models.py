from django.db import models
from django.db.models import Q, Avg


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    sku = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return self.name


class PriceHistory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="prices"
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{str(self.id)}: {str(self.product)}"

    @staticmethod
    def set_category_price(queryset, price):
        queryset.update(price=price)
        return queryset

    @staticmethod
    def calculate_average_price_for_period(queryset, validated_data):
        category_name, product_name, start_date, end_date = validated_data.values()
        if category_name and product_name:
            queryset = queryset.filter(category__name__icontains=category_name).filter(
                name__icontains=product_name
            )
        elif category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        elif product_name:
            queryset = queryset.filter(name__icontains=product_name)
        return (
            queryset.filter(
                Q(prices__start_date__gte=start_date)
                & Q(prices__end_date__lte=end_date)
            )
            .annotate(avg_product_price=Avg("prices__price"))
            .values("name", "avg_product_price")
        )
