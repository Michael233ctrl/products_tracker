from rest_framework import serializers

from core.models import Category, Product, PriceHistory


class AveragePriceForPeriodResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    avg_product_price = serializers.DecimalField(max_digits=7, decimal_places=2)


class AveragePriceForPeriodSerializer(serializers.Serializer):
    category = serializers.CharField(required=False, allow_null=True)
    product = serializers.CharField(required=False, allow_null=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                "'end_date' must be bigger than 'start_date'"
            )
        return attrs


class SetCategoryPriceSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=7, decimal_places=2)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ("id", "product", "price", "created_at", "start_date", "end_date")


class ProductSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "category", "sku", "description", "prices")


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "products")
