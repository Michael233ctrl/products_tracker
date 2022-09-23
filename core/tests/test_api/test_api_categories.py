import json

from django.urls import reverse
from rest_framework import status

from core.models import Category
from core.serializers import CategorySerializer
from core.tests.test_api.test_base import BaseApiTestCase


class CategoryApiTestCase(BaseApiTestCase):
    def test_get_success(self):
        url = reverse("categories-list")
        response = self.client.get(url)
        serializer_data = CategorySerializer(
            [self.category_1, self.category_2], many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_create_success(self):
        url = reverse("categories-list")
        data = {"name": "Test category 3"}
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Category.objects.count())

    def test_get_detail_success(self):
        url = reverse("categories-detail", args=(self.category_1.id,))
        response = self.client.get(url)
        serializer_data = CategorySerializer(self.category_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_detail_fail(self):
        url = reverse("categories-detail", args=(1221,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_success(self):
        url = reverse("categories-detail", args=(self.category_1.id,))
        data = {"name": f"Updated {self.category_1.name}"}
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], f"Updated {self.category_1.name}")

    def test_delete_success(self):
        url = reverse("categories-detail", args=(self.category_1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(1, Category.objects.count())
