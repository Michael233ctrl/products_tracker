import json

from django.urls import reverse
from rest_framework import status

from core.models import Product
from core.serializers import ProductSerializer
from core.tests.test_api.test_base import BaseApiTestCase


class ProductApiTestCase(BaseApiTestCase):
    def test_get_success(self):
        url = reverse("products-list")
        response = self.client.get(url)
        serializer_data = ProductSerializer(
            [self.product_1, self.product_2], many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_create_success(self):
        url = reverse("products-list")
        data = {
            "name": "Test product 3",
            "category": self.category_1.id,
            "sku": 13,
            "description": "product description",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Product.objects.count())

    def test_create_fail(self):
        url = reverse("products-list")
        data = {
            "name": "Test product 3",
            "category": 13,
            "sku": 13,
            "description": "product description",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_detail_success(self):
        url = reverse("products-detail", args=(self.product_1.id,))
        response = self.client.get(url)
        serializer_data = ProductSerializer(self.product_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_detail_fail(self):
        url = reverse("products-detail", args=(21,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_success(self):
        url = reverse("products-detail", args=(self.product_1.id,))
        data = {
            "name": f"Updated {self.product_1.name}",
            "category": self.category_1.id,
            "sku": 13,
            "description": "product description",
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], f"Updated {self.product_1.name}")

    def test_patch_success(self):
        url = reverse("products-detail", args=(self.product_1.id,))
        data = {"sku": 15}
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["sku"], 15)

    def test_patch_fail(self):
        url = reverse("products-detail", args=(self.product_1.id,))
        data = {"sku": -15}
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_success(self):
        url = reverse("products-detail", args=(self.product_1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Product.objects.count())
