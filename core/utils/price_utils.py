from django.db.models import Avg, Q


def set_category_price(queryset, price):
    queryset.update(price=price)
    return queryset


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
            Q(prices__start_date__gte=start_date) & Q(prices__end_date__lte=end_date)
        )
        .annotate(avg_product_price=Avg("prices__price"))
        .values("name", "avg_product_price")
    )
