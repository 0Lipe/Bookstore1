import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()

        self.product = ProductFactory(
            title='pro controller',
            price=200.00,
        )

    def test_get_all_product(self):
        response = self.client.get(
            reverse('product-list', kwargs={'version': 'v1'})
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)
        self.assertEquals(product_data['product'][0]['title'], self.product.title)
        self.assertEquals(product_data['product'][0]['price'], self.product.price)
        self.assertEquals(product_data['product'][0]['active'], self.product.active)
        self.assertEquals(product_data['product'][0]['category']['title'], self.category.title)

    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'title': 'notebook',
            'price': 800.00,
            'categories_id' : [ category.id ]
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type = 'application/json'
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title='notebook')


        self.assertEquals(created_product.title, 'notebook')
        self.assertEquals(created_product.price, 800.00)

    