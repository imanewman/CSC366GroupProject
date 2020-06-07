from django.test import TestCase
from django import db
import datetime

from business.models import Ingredients, MenuItem, \
    LineItem, StockItem, Refund, Receipt, Employee, \
    Customer, Location


class MenuItemsTestCase(TestCase):
    #############
    # Menu Item #
    #############
    def test_create_menu_item(self):
        self.assertEqual(MenuItem.objects.count(), 0)
        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        menu_item.items.set([item])

        self.assertEqual(MenuItem.objects.count(), 1)


    def test_delete_menu_item_cascade_delete_ingredients_lineItem(self):
        self.assertEqual(LineItem.objects.count(), 0)

        employee = Employee.objects.create(
            emplId=4543,
            name="test name",
            contact="410293049"
        )

        customer = Customer.objects.create(
            name="customer name",
            email="customer.test@gmail.com",
            joinDate= datetime.date(2020, 6, 1),
            points= 3
        )
        
        location = Location.objects.create(
            name="test location 0"
        )

        data = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }

        receipt = Receipt.objects.create(**data)

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        Line_item = LineItem.objects.create(
            receipt=receipt,
            ordinal=2,
            menuItem=menu_item,
            qty=0
        )

        menu_item.items.set([item])

        self.assertEqual(MenuItem.objects.count(), 1)
        self.assertEqual(Ingredients.objects.count(), 1)
        self.assertEqual(LineItem.objects.count(), 1)

        menu_item.delete()
        self.assertEqual(MenuItem.objects.count(), 0)
        self.assertEqual(Ingredients.objects.count(), 0)
        self.assertEqual(LineItem.objects.count(), 0)


    ###############
    # Ingredients #
    ###############
    def test_create_ingredients(self):
        self.assertEqual(Ingredients.objects.count(), 0)

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        menu_item.items.set([item])
        
        self.assertEqual(Ingredients.objects.count(), 1)

    def test_delete_ingredient_dont_cascade_delete_menu_item(self):
        self.assertEqual(Ingredients.objects.count(), 0)
        self.assertEqual(MenuItem.objects.count(), 0)

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        menu_item.items.set([item])
        
        self.assertEqual(Ingredients.objects.count(), 1)
        self.assertEqual(MenuItem.objects.count(), 1)

        ingredients.delete()
        self.assertEqual(Ingredients.objects.count(), 0)
        self.assertEqual(MenuItem.objects.count(), 1)


    #############
    # Line Item #
    #############
    def test_create_line_item(self):
        self.assertEqual(LineItem.objects.count(), 0)

        employee = Employee.objects.create(
            emplId=4543,
            name="test name",
            contact="410293049"
        )

        customer = Customer.objects.create(
            name="customer name",
            email="customer.test@gmail.com",
            joinDate= datetime.date(2020, 6, 1),
            points= 3
        )
        
        location = Location.objects.create(
            name="test location 0"
        )

        data = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }

        receipt = Receipt.objects.create(**data)

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        line_item = LineItem.objects.create(
            receipt=receipt,
            ordinal=2,
            menuItem=menu_item,
            qty=0
        )

        menu_item.items.set([item])

        self.assertEqual(LineItem.objects.count(), 1)

    def test_delete_line_item_dont_cascade_delete_menu_item(self):
        self.assertEqual(LineItem.objects.count(), 0)
        self.assertEqual(MenuItem.objects.count(), 0)

        employee = Employee.objects.create(
            emplId=4543,
            name="test name",
            contact="410293049"
        )

        customer = Customer.objects.create(
            name="customer name",
            email="customer.test@gmail.com",
            joinDate= datetime.date(2020, 6, 1),
            points= 3
        )
        
        location = Location.objects.create(
            name="test location 0"
        )

        data = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }

        receipt = Receipt.objects.create(**data)

        item = StockItem.objects.create(
            name="test stock item 0"
        )

        menu_item = MenuItem.objects.create(
            name= "test name 0",
            price= 2.30
        )

        ingredients = Ingredients.objects.create(
            stockItem= item,
            menuItem= menu_item,
            qty= 3
        )

        line_item = LineItem.objects.create(
            receipt=receipt,
            ordinal=2,
            menuItem=menu_item,
            qty=0
        )

        menu_item.items.set([item])
        
        self.assertEqual(LineItem.objects.count(), 1)
        self.assertEqual(MenuItem.objects.count(), 1)

        line_item.delete()
        self.assertEqual(LineItem.objects.count(), 0)
        self.assertEqual(MenuItem.objects.count(), 1)
