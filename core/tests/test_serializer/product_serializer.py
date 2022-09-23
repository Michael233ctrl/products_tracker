from rest_framework.test import APITestCase

from core.models import Category, Product
from core.serializers import ProductSerializer


class ProductSerializerTestCase(APITestCase):
    def test_success(self):
        cat_1 = Category.objects.create(name="Test serializer category 1")
        prod_1 = Product.objects.create(
            name="Test serializer product 1",
            category=cat_1,
            sku=12,
            description="Desc for product 1",
        )
        serializer_data = ProductSerializer([prod_1], many=True).data
        expected_data = [
            {
                "id": prod_1.id,
                "name": "Test serializer product 1",
                "category": cat_1.id,
                "sku": 12,
                "description": "Desc for product 1",
                "prices": [],
            },
        ]
        self.assertEqual(serializer_data, expected_data)
