import json

from django.urls import reverse
from rest_framework import status

from core.models import PriceHistory
from core.tests.test_api.test_base import BaseApiTestCase


class PriceApiTestCase(BaseApiTestCase):
    def test_create(self):
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
