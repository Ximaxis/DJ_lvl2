from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from authnapp.models import ShopUser
from mainapp.models import Products, ProductCategory


class TestMainappSmoke(TestCase):
    fixtures = [
        "categories",
        "products",
        "admin",
    ]

    def setUp(self):
        self.client = Client()

    def test_fixtures_load(self):
        # Check fixtures loading
        self.assertGreater(ProductCategory.objects.count(), 0)
        self.assertGreater(Products.objects.count(), 0)

    def test_mainapp_urls(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/shop/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/shop/category/all/")
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f"/shop/category/{category.slug}/")
            self.assertEqual(response.status_code, 200)

        for product in Products.objects.all():
            response = self.client.get(f"/shop/{product.slug}/")
            self.assertEqual(response.status_code, 200)


class ProductsTestCase(TestCase):
    def test_product_print(self):
        product_1 = Products.objects.get(title="New Woman Wearing Dress")
        product_2 = Products.objects.get(title="Old Woman Wearing Dress")
        self.assertEqual(str(product_1), "New Woman Wearing Dress (Женская одежда)")
        self.assertEqual(str(product_2), "Old Woman Wearing Dress (Женская одежда)")

    def test_product_get_items(self):
        product_1 = Products.objects.get(title="New Woman Wearing Dress")
        product_3 = Products.objects.get(title="Night Woman Wearing Dress")

        products_as_class_method = set(product_1.get_items())
        products = set([product_1, product_3])

        self.assertIsNotNone(products_as_class_method.intersection(products))
