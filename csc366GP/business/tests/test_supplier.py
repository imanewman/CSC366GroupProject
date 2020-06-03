from django.test import TestCase
from django import db

from business.models import Supplier, StockItem, \
    SupplierInvoice, Location, SupplierInvoiceLine


class SupplierTestCase(TestCase):
    #############
    # Suppliers #
    #############
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

    ###############
    # Stock Items #
    ###############
    def test_create_stock_item(self):
        data = {
            "name": "test stock item 0"
        }

        self.assertEqual(StockItem.objects.count(), 0)

        StockItem.objects.create(**data)

        self.assertEqual(StockItem.objects.count(), 1)

        item = StockItem.objects.get(name=data["name"])

        self.assertEqual(item.name, data["name"])

    ############
    # Invoices #
    ############
    def test_fail_create_supplier_invoice_no_supplier(self):
        data = {
            "supplierId": "",
            "location": "",
            "amount": 1,
            "date": "2020-06-03"
        }

        self.assertRaises(
            ValueError,
            lambda : SupplierInvoice.objects.create(**data)
        )

    def test_fail_create_supplier_invoice_no_location(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        data = {
            "supplierId": supplier,
            "location": "",
            "amount": 1,
            "date": "2020-06-03"
        }

        self.assertRaises(
            ValueError,
            lambda : SupplierInvoice.objects.create(**data)
        )

    def test_create_supplier_invoice_no_items(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        location = Location.objects.create(
            name="test location 0"
        )

        data = {
            "supplierId": supplier,
            "location": location,
            "amount": 1,
            "date": "2020-06-03"
        }

        self.assertEqual(SupplierInvoice.objects.count(), 0)

        SupplierInvoice.objects.create(**data)

        self.assertEqual(SupplierInvoice.objects.count(), 1)

    # test that creating an invoice and linking an item fails
    # without first having an invoice line
    def test_fail_create_supplier_invoice_no_lines(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        location = Location.objects.create(
            name="test location 0"
        )

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        invoice = SupplierInvoice.objects.create(
            supplierId=supplier,
            location=location,
            amount=1,
            date="2020-06-03"
        )

        self.assertRaises(
            db.utils.IntegrityError,
            lambda: invoice.items.set([item])
        )

    #################
    # Invoice Lines #
    #################
    def test_create_supplier_invoice_1_item(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        location = Location.objects.create(
            name="test location 0"
        )

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        invoice = SupplierInvoice.objects.create(
            supplierId=supplier,
            location=location,
            amount=1,
            date="2020-06-03"
        )

        SupplierInvoiceLine.objects.create(
            stockItem=item,
            supplierInvoice=invoice,
            qty=1,
            costPerItem=10
        )

        invoice.items.set([item])

        self.assertEqual(invoice.items.get(), item)

    # tests that deleting a supplier also deletes invoices from them
    def test_delete_supplier_cascade_invoice(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        location = Location.objects.create(
            name="test location 0"
        )

        data = {
            "supplierId": supplier,
            "location": location,
            "amount": 1,
            "date": "2020-06-03"
        }

        self.assertEqual(SupplierInvoice.objects.count(), 0)

        SupplierInvoice.objects.create(**data)

        self.assertEqual(SupplierInvoice.objects.count(), 1)

        supplier.delete()

        self.assertEqual(Supplier.objects.count(), 0)
        self.assertEqual(SupplierInvoice.objects.count(), 0)
        self.assertEqual(Location.objects.count(), 1)

    # tests that deleting a supplier also deletes lines of related invoices
    def test_delete_supplier_cascade_invoice_lines(self):
        supplier = Supplier.objects.create(
            email="test_suppier_0@calpoly.edu",
            name="test supplier 0"
        )

        location = Location.objects.create(
            name="test location 0"
        )

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        invoice = SupplierInvoice.objects.create(
            supplierId=supplier,
            location=location,
            amount=1,
            date="2020-06-03"
        )

        SupplierInvoiceLine.objects.create(
            stockItem=item,
            supplierInvoice=invoice,
            qty=1,
            costPerItem=10
        )

        invoice.items.set([item])

        supplier.delete()

        self.assertEqual(Supplier.objects.count(), 0)
        self.assertEqual(SupplierInvoice.objects.count(), 0)
        self.assertEqual(SupplierInvoiceLine.objects.count(), 0)
        self.assertEqual(StockItem.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)
