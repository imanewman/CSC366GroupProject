from django.test import TestCase
from django import db
import datetime

from business.models import Employee, Customer, Receipt, MenuItem, Location, StockItem, LineItem


class ReceiptTestCases(TestCase):
    #############
    # Customer #
    #############
    def test_create_customer(self):
        data = {
            "name": "Yusuf B",
            "email": "yusuf.b",
            "joinDate":  datetime.date(2020, 6, 1),
            "points": 3
        }

        self.assertEqual(Customer.objects.count(), 0)

        Customer.objects.create(**data)

        self.assertEqual(Customer.objects.count(), 1)

        customer = Customer.objects.get(name=data["name"])

        self.assertEqual(customer.name, data["name"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.joinDate, data["joinDate"])
        self.assertEqual(customer.points, data["points"])
        

    #############
    # Employee #
    #############
    def test_create_employee(self):
        data = {
            "emplId": 394,
            "name": "yusuf",
            "contact": "410839423"
        }

        self.assertEqual(Employee.objects.count(), 0)

        Employee.objects.create(**data)

        self.assertEqual(Employee.objects.count(), 1)

        employee = Employee.objects.get(name=data["name"])

        self.assertEqual(employee.emplId, data["emplId"])
        self.assertEqual(employee.name, data["name"])
        self.assertEqual(employee.contact, data["contact"])


    #############
    # Receipt #
    #############

    #tests successful creation and link of receipt table, location table, customer table, and employee table
    def test_create_receipt(self):
        
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

        self.assertEqual(Receipt.objects.count(), 0)

        Receipt.objects.create(**data)

        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Employee.objects.count(), 1)


    #Tests Deletion of Location causes Deletion of Receipt
    def test_create_receipt_delete_Location(self):
        
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

        self.assertEqual(Receipt.objects.count(), 0)

        Receipt.objects.create(**data)

        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Employee.objects.count(), 1)

        location.delete()
        self.assertEqual(Receipt.objects.count(), 0)

    #test no employee with Receipt Creation
    def test_create_receipt_no_employee(self):

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
            "employee" : "",
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }
        
        self.assertRaises(
            ValueError,
            lambda: Receipt.objects.create(**data)
        )

    #test no location with Receipt Creation
    def test_create_receipt_no_location(self):
        
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
        
        data = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : ""
        }

        self.assertRaises(
            ValueError,
            lambda: Receipt.objects.create(**data)
        )

    #############
    # Receipt & Line Item #
    #############

    #tests successful creation and link of lineItem with Receipt
    def test_create_receipt_with_LineItem(self):
    
        #create MenuItem
        data = {
            "name" : "hi",
            "price": float(3.24)
        }

        self.assertEqual(MenuItem.objects.count(), 0)

        menuItem = MenuItem.objects.create(**data)

        self.assertEqual(MenuItem.objects.count(), 1)


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
        
        #create receipt
        data2 = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }

        self.assertEqual(Receipt.objects.count(), 0)

        receipt = Receipt.objects.create(**data2)

        #create lineItem
        data3 = {
            "receipt" : receipt,
            "ordinal": 32,
            "menuItem": menuItem,
            "qty": 1
        }

        self.assertEqual(LineItem.objects.count(), 0)

        LineItem.objects.create(**data3)

        self.assertEqual(LineItem.objects.count(), 1)


    #tests successful DELETION of lineItem after deletion of receipt 
    def test_create_receipt_with_LineItem_Delete(self):
    
        #create MenuItem
        data = {
            "name" : "hi",
            "price": float(3.24)
        }

        self.assertEqual(MenuItem.objects.count(), 0)

        menuItem = MenuItem.objects.create(**data)

        self.assertEqual(MenuItem.objects.count(), 1)


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
        
        #create receipt
        data2 = {
            "employee" : employee,
            "customer" : customer,
            "tax" : float(21.35),
            "tip" : float(343.92),
            "total" : float(34.24),
            "date" : datetime.date(2020, 7, 1),
            "payment": "Card",
            "location" : location
        }

        self.assertEqual(Receipt.objects.count(), 0)

        receipt = Receipt.objects.create(**data2)

        #create lineItem
        data3 = {
            "receipt" : receipt,
            "ordinal": 32,
            "menuItem": menuItem,
            "qty": 1
        }

        self.assertEqual(LineItem.objects.count(), 0)

        LineItem.objects.create(**data3)

        self.assertEqual(LineItem.objects.count(), 1)

        receipt.delete()

        self.assertEqual(LineItem.objects.count(), 0)

  