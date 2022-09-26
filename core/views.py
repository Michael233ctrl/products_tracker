from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core import serializers
from core.models import Category, Product, PriceHistory
from core.utils.price_utils import (
    calculate_average_price_for_period,
    set_category_price,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related("products")
    serializer_class = serializers.CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("prices")
    serializer_class = serializers.ProductSerializer


class PriceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = serializers.PriceSerializer

    @swagger_auto_schema(
        query_serializer=serializers.AveragePriceForPeriodSerializer,
        responses={
            status.HTTP_200_OK: serializers.AveragePriceForPeriodResponseSerializer
        },
    )
    @action(
        detail=False,
        methods=["GET"],
        serializer_class=serializers.AveragePriceForPeriodSerializer,
        name="calculate_average_price_for_period",
    )
    def calculate_average_price_for_period(self, request, *args, **kwargs):
        """
        Calculate the average price for a period for a product or an entire category
        """
        queryset = Product.objects.all()
        data = {
            **request.data,
            "category": request.query_params.get("category"),
            "product": request.query_params.get("product"),
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        avg_price = calculate_average_price_for_period(
            queryset, serializer.validated_data
        )
        response_serializer = serializers.AveragePriceForPeriodResponseSerializer(
            avg_price, many=True
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: serializers.PriceSerializer},
    )
    @action(
        detail=True,
        methods=["PATCH"],
        serializer_class=serializers.SetCategoryPriceSerializer,
        name="set_category_price",
    )
    def set_category_price(self, request, *args, **kwargs):
        """Set price for entire products"""
        queryset = self.get_queryset().filter(product__category=kwargs.get("pk"))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products = set_category_price(queryset, serializer.validated_data["price"])
        response_serializer = serializers.PriceSerializer(products, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
