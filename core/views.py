from django.db.models import Avg, Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core import serializers
from core.models import Category, Product, PriceHistory


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().prefetch_related("products")
    serializer_class = serializers.CategorySerializer

    @swagger_auto_schema(
        query_serializer=serializers.AveragePriceForPeriodSerializer,
        responses={status.HTTP_200_OK: serializers.AveragePriceForPeriodSerializer},
    )
    @action(
        detail=True,
        methods=["GET"],
        serializer_class=serializers.AveragePriceForPeriodSerializer,
        name="average_price_for_period",
    )
    def average_price_for_period(self, request, *args, **kwargs):
        """Calculate average product price for period"""
        category = self.get_object()
        data = {
            **request.data,
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        queryset = (
            Product.objects.filter(category=category)
            .filter(
                Q(prices__start_date__gte=serializer.validated_data["start_date"])
                & Q(prices__start_date__lte=serializer.validated_data["end_date"])
            )
            .annotate(avg_product_price=Avg("prices__price"))
            .values("name", "avg_product_price")
        )
        response_serializer = serializers.AveragePriceForPeriodResponseSerializer(
            queryset, many=True
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().prefetch_related("prices")
    serializer_class = serializers.ProductSerializer


class PriceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = PriceHistory.objects.order_by("-created_at")
    serializer_class = serializers.PriceSerializer
