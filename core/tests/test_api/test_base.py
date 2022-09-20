import datetime

from rest_framework.test import APITestCase

from core.models import Category, Product, PriceHistory


class BaseApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.category_1 = Category.objects.create(name="Test category 1")
        self.category_2 = Category.objects.create(name="Test category 2")

        self.product_1 = Product.objects.create(
            name="Test product 1",
            category=self.category_1,
            sku=12,
            description="Desc for product 1",
        )
        self.product_2 = Product.objects.create(
            name="Test product 2",
            category=self.category_2,
            sku=12,
            description="Desc for product 2",
        )

        self.product_1_price_history_1 = PriceHistory.objects.create(
            product=self.product_1,
            price=12,
            start_date=datetime.datetime.strptime("2020-09-01", "%Y-%m-%d"),
            end_date=datetime.datetime.strptime("2021-09-01", "%Y-%m-%d"),
        )
        self.product_1_price_history_2 = PriceHistory.objects.create(
            product=self.product_1,
            price=9.99,
            start_date=datetime.datetime.strptime("2021-09-01", "%Y-%m-%d"),
            end_date=datetime.datetime.strptime("2022-09-01", "%Y-%m-%d"),
        )
