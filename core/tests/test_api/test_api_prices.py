import json

from django.urls import reverse
from rest_framework import status

from core.models import PriceHistory
from core.tests.test_api.test_base import BaseApiTestCase


class PriceApiTestCase(BaseApiTestCase):
    def test_create_success(self):
        url = reverse("prices-list")
        data = {
            "product": self.product_2.id,
            "price": "13.99",
            "start_date": "2022-07-20",
            "end_date": "2022-08-20",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, PriceHistory.objects.count())

    def test_calculate_average_price_for_period_for_category_success(self):
        start_date = "2020-01-01"
        end_date = "2022-09-01"
        url = (
            reverse("prices-list") + "calculate_average_price_for_period/"
            f"?category={self.category_1.name}&start_date={start_date}&end_date={end_date}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.product_1.name)

    def test_calculate_average_price_for_period_for_product_success(self):
        start_date = "2020-01-01"
        end_date = "2022-09-01"
        url = (
            reverse("prices-list") + "calculate_average_price_for_period/"
            f"?product={self.product_1.name}&start_date={start_date}&end_date={end_date}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calculate_average_price_for_period_for_product_category_success(self):
        start_date = "2020-01-01"
        end_date = "2022-09-01"
        url = (
            reverse("prices-list") + "calculate_average_price_for_period/"
            f"?category={self.category_1.name}&product={self.product_1.name}"
            f"&start_date={start_date}&end_date={end_date}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.product_1.name)

    def test_calculate_average_price_for_period_fail_data(self):
        start_date = "2022-01-01"
        end_date = "2020-09-01"
        url = (
            reverse("prices-list") + "calculate_average_price_for_period/"
            f"?category={self.category_1.name}&start_date={start_date}&end_date={end_date}"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_category_price_success(self):
        url = reverse("prices-list") + f"{self.category_1.id}/set_category_price/"
        data = {"price": "18.99"}
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["price"], data["price"])
