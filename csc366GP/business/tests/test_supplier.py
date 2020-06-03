from django.test import TestCase

from business.models import Supplier, StockItem


class SupplierTestCase(TestCase):
    def test_create_supplier(self):
        data = {
            "email": "test_suppier_0@calpoly.edu",
            "name": "test supplier 0"
        }

        self.assertEqual(Supplier.objects.count(), 0)

        Supplier.objects.create(**data)

        self.assertEqual(Supplier.objects.count(), 1)

        supplier = Supplier.objects.get(name=data["name"])

        self.assertEqual(supplier.email, data["email"])
        self.assertEqual(supplier.name, data["name"])

    def test_create_stock_item(self):
        data = {
            "name": "test stock item 0"
        }
        
        self.assertEqual(StockItem.objects.count(), 0)
        
        StockItem.objects.create(**data)
        
        self.assertEqual(StockItem.objects.count(), 1)
        
        item = StockItem.objects.get(name=data["name"])
        
        self.assertEqual(item.name, data["name"])