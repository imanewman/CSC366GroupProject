from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Employee(models.Model):
   emplId = models.PositiveIntegerField(primary_key=True)
   name = models.CharField(max_length=100)
   contact = models.CharField(max_length=15) #phone number

class PayCheck(models.Model):
   #have to make payCheck before you can log time cards
   startDate = models.DateField()
   endDate = models.DateField()
   total = models.FloatField(blank = True)
   emplId = models.ForeignKey(Employee, models.SET_NULL, null=True, to_field="emplId")

class DailyTimeCard(models.Model):
   date = models.DateField()
   emplId = models.ForeignKey(Employee, models.SET_NULL, null= True, to_field = "emplId")
   hours = models.FloatField()
   rate = models.FloatField()

   payCheck = models.ForeignKey(PayCheck, on_delete=models.CASCADE, default = 0)

class Location(models.Model):
   city = models.CharField(max_length=100, blank = True)
   state = models.CharField(max_length=100, blank = True)
   name = models.CharField(max_length=100, blank = True)

class LocationExpenses(models.Model):
   month = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(1), MinValueValidator(12)]
     )
   location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)
   year = models.PositiveIntegerField()
   amount = models.FloatField()
   expenseName = models.CharField(max_length=200)

class EmployementRecod(models.Model):
   emplId = models.ForeignKey(Employee, models.SET_NULL, null=True, to_field="emplId")
   startDate = models.DateField()
   endDate = models.DateField(blank = True)
   position = models.CharField(max_length=25, choices=(("M", "Manager"), ("E", "Base Employee")), default='Base Employee')
   role = models.CharField(max_length=100, default="unassigned")

   #self manager loop on self, can be null if you are a manager
   manager = models.ForeignKey("self", on_delete=models.CASCADE, null = True, related_name='employee')
   location = models.ForeignKey(Location, on_delete=models.CASCADE, default = 0)

class Customer(models.Model):
   name = models.CharField(max_length=100, blank=True)
   email = models.CharField(max_length=100, blank = True)
   joinDate = models.DateField()
   points = models.IntegerField(default = 0)

class Receipt(models.Model):
   employee = models.ForeignKey(Employee, models.SET_NULL, null=True, to_field="emplId")
   customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
   tax = models.FloatField()
   tip = models.FloatField()
   total = models.FloatField()
   date = models.DateField()
   payment = models.CharField(max_length=25, choices=(("Crd", "Card"), ("Csh", "Cash")))
   location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)

class Supplier(models.Model):
   name = models.CharField(max_length=100)
   email = models.CharField(max_length=100)

class StockItem(models.Model):
   name = models.CharField(max_length=100)

class SupplierInvoice(models.Model):
   supplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=0)
   location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)
   amount = models.FloatField()
   date = models.DateField()
   items = models.ManyToManyField(StockItem, through = 'SupplierInvoiceLine')

class SupplierInvoiceLine(models.Model):
   stockItem = models.ForeignKey(StockItem, on_delete=models.CASCADE, default=0)
   supplierInvoice = models.ForeignKey(SupplierInvoice, on_delete=models.CASCADE, default=0)
   qty = models.IntegerField()
   costPerItem = models.FloatField()

class Inventory(models.Model):
   location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)
   stockItem = models.ForeignKey(StockItem, on_delete=models.CASCADE, default=0)
   qty = models.IntegerField()

class MenuItem(models.Model):
   name = models.CharField(max_length=100)
   price = models.FloatField()
   items = models.ManyToManyField(StockItem, through = 'Ingredients')

class Ingredients(models.Model):
   stockItem = models.ForeignKey(StockItem, on_delete=models.CASCADE, default=0)
   menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default=0)
   qty = models.PositiveIntegerField()

class LineItem(models.Model):
   receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, default = 0)
   ordinal = models.IntegerField()
   menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default = 0)
   qty = models.IntegerField()

class Refund(models.Model):
   receiptItem = models.ForeignKey(LineItem, on_delete=models.CASCADE, default=0)
   #removed the ordinal part since our uml already pointed from the lineitem (which has ordinal)
   #ordinal = models.IntegerField()
   employee = models.ForeignKey(Employee, models.SET_NULL, null=True, to_field="emplId")
   returnDate = models.DateField()
   qty = models.IntegerField()