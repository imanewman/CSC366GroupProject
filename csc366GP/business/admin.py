from django.contrib import admin
from .models import *
# Register your models here.
#admin.site.register(TableName)
admin.site.register(Employee)
admin.site.register(PayCheck)
admin.site.register(DailyTimeCard)
admin.site.register(Location)
admin.site.register(LocationExpenses)
admin.site.register(EmploymentRecord)
admin.site.register(Customer)
admin.site.register(Receipt)
admin.site.register(Supplier)
admin.site.register(StockItem)
admin.site.register(SupplierInvoice)
admin.site.register(SupplierInvoiceLine)
admin.site.register(Inventory)
admin.site.register(MenuItem)
admin.site.register(Ingredients)
admin.site.register(LineItem)
admin.site.register(Refund)