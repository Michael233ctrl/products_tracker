from rest_framework.test import APITestCase

from core.models import Category
from core.serializers import CategorySerializer


class CategorySerializerTestCase(APITestCase):
    def test_ok(self):
        cat_1 = Category.objects.create(name="Test serializer category 1")
        cat_2 = Category.objects.create(name="Test serializer category 2")
        serializer_data = CategorySerializer([cat_1, cat_2], many=True).data
        expected_data = [
            {"id": cat_1.id, "name": "Test serializer category 1", "products": []},
            {"id": cat_2.id, "name": "Test serializer category 2", "products": []},
        ]
        self.assertEqual(serializer_data, expected_data)
